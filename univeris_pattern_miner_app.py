from common_imports import *
from constants import *
from data_converter import convert_to_transactions
from pattern_miner import mine_patterns
from data_requester import get_univeris_data, get_data_params


EXTERNAL_STYLESHEETS  = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
YEARS  = [i for i in (range(2010, 2023))]


app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS )
params = asyncio.run(get_data_params(YEARS ))

files = {JOURNALS_FILE_NAME: None, STUDENTS_FILE_NAME: None, 
         GRADES_FILE_NAME: None, RATINGS_FILE_NAME: None, EGE_FILE_NAME: None}

patterns = None

from pages.layout_find_patterns_page import layout_find_patterns_page
from pages.url_bar_and_content_div import url_bar_and_content_div
from pages.layout_get_data_page import layout_get_data_page
 
app.layout = url_bar_and_content_div

app.validation_layout = html.Div([
    url_bar_and_content_div,
    layout_find_patterns_page,
    layout_get_data_page
])

# TODO Сделать единую систему отображения предупреждений

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/get-data":
        return layout_get_data_page
    else:
        return layout_find_patterns_page
    
    
@app.callback(
    Output('year-dropdown', 'options'),
    [Input('url', 'pathname')]
)
def update_dropdown_options(pathname):
    if pathname == '/get-data': 
        options = [{'label': year, 'value': year} for year in params["Year"].unique()]
        return options
    return []


@app.callback(Output("download-dataframe-xlsx", "data"),
          Input("export-btn", "n_clicks"),
          State('excel-filename-input', "value"),
          prevent_initial_call=True)
def download_excel_patterns(n_clicks: int, filename: str):
    if (n_clicks > 0 
        and isinstance(patterns, pd.DataFrame) 
        and filename 
        and filename != ""):
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        return dcc.send_data_frame(patterns.to_excel, 
                                   filename, 
                                   sheet_name="Sheet_name_1")

def check_data_files():
    found_files = []
    missing_files = []
    for filename, data in files.items():
        if data is not None:
            found_files.append(filename)
        else:
            missing_files.append(filename)
    
    missing_files = ", ".join(missing_files)
    found_files = ", ".join(found_files)

    return found_files, missing_files


def parse_json_data(contents, filenames):   
    for content, filename in zip(contents, filenames):
        if filename not in files.keys():
            return html.Div(["Неверное имя загружаемого файла"])
        try:
            content_type, content_string = content.split(',')
            decoded = base64.b64decode(content_string)

            if filename.endswith('.zip'):
                zip_str = io.BytesIO(decoded)
                zip_data = zipfile.ZipFile(zip_str)
                for json_file in zip_data.infolist():
                    if json_file.filename in files:
                        json_data = zip_data.read(json_file)
                        json_data = json.loads(json_data)
                        df = pd.DataFrame(json_data)
                        files[json_file.filename] = df
            else:
                json_data = json.loads(decoded)
                df = pd.DataFrame(json_data)
                files[filename] = df
        except Exception as e:
            print(e)
            return html.Div([f"Ошибка при обработке файла {filename}"])
    
    
@app.callback(Output('output-upload-json-data', 'children'),
              Input('upload-json-data', 'contents'),
              State('upload-json-data', 'filename'))
def update_file_availability_output(contents, names):
    warning = html.Div()
    if contents is not None:
        warning = parse_json_data(contents, names)
    found_files, missing_files = check_data_files()
    if len(missing_files) == 0:
        return html.Div([
            warning,
            f"Найдены все нужные файлы: {found_files}"
            ])
    elif len(found_files) == 0:
        return html.Div([
            warning,
            f"Добавьте файлы: {missing_files}"
            ])
    else:
        return html.Div([
            warning,
            html.Div(f"Найдены файлы: {found_files}"),
            html.Div(f"Добавьте файлы: {missing_files}")
            ])

    
@app.callback(Output('output-search-btn', 'children'),
              Input('search-btn', 'n_clicks'),
              State('sup', 'value'),
              State('conf', 'value'),
              State('lift', 'value'),
              State('left_el', 'value'),
              State('right_el', 'value'))
def get_patterns(n_clicks, sup, conf, lift, max_left_elements, max_right_elements):
    global patterns
    if n_clicks > 0:
        # Checking files
        for value in files.values():
            if not isinstance(value, pd.DataFrame):
                return html.Span("Загружены не все файлы", id="notification", style={})
            if len(value) < 30:
                return html.Span("В вашей выборке слишком мало данных", id="notification", style={})
            
        if not (0 < sup < 1):
            return html.Span("Поддержка должна быть от 0 до 1", id="notification", style={})
        if not (0 < conf < 1):
            return html.Span("Доставерность должна быть от 0 до 1", id="notification", style={})
        if lift < 1:
            return html.Span("Подъем должен быть минимум 1", id="notification", style={})
        if max_left_elements < 1:
            return html.Span("Антецедент может состояить минимум из одного элемента", id="notification", style={})
        if max_right_elements < 1:
            return html.Span("Консеквент может состояить минимум из одного элемента", id="notification", style={})

        # Getting transactions
        transactions = convert_to_transactions(
           files[JOURNALS_FILE_NAME],
           files[STUDENTS_FILE_NAME],
           files[EGE_FILE_NAME],
           files[GRADES_FILE_NAME],
           files[RATINGS_FILE_NAME]  
        )
        patterns = mine_patterns(transactions, sup, lift, conf, max_left_elements, max_right_elements)

        # Возвращение результатов в виде таблицы
        return dash_table.DataTable(patterns.to_dict('records'),
                                    [{"name": i, "id": i} for i in patterns.columns], 
                                    id='tbl',
                                    filter_action="native",
                                    sort_action="native",
                                    sort_mode="multi",
                                    style_data={
                                        'width': '100px', 'minWidth': '100px', 'maxWidth': '700px',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',
                                        'font-size': '16px',
                                    },
                                    style_header={
                                        'fontSize': '18px',
                                    },
                                    style_filter={
                                        'fontSize': '18px',
                                    })


@app.callback(
    Output('qualification-dropdown', 'options'),
    Input('year-dropdown', 'value')
)
def update_dish_dropdown(selected_years):
    if selected_years:
        selected_params = params[params["Year"].isin(selected_years)]
        options = [{'label': qualifiation, 'value': qualifiation} for qualifiation in selected_params["Speciality"].unique()]
    else:
        options = []
    return options


@app.callback(
    Output('directions-dropdown', 'options'),
    Input('qualification-dropdown', 'value'),
    State('year-dropdown', 'value')
)
def update_dish_dropdown(selected_qualifications, selected_years):
    if selected_qualifications:
        selected_params = params[params["Year"].isin(selected_years)]
        selected_params = selected_params[selected_params["Speciality"].isin(selected_qualifications)]
        options = [{'label': specialization, 'value': specialization} for specialization in selected_params["DirectionName"].unique()]
    else:
        options = []
    return options


@app.callback(Output('output-get-data-btn', 'children'),
              Input('get-data-btn', 'n_clicks'),
              State('year-dropdown', 'value'),
              State('qualification-dropdown', 'value'),
              State('directions-dropdown', 'value'))
def get_data_from_api(n_clicks, years, qualifications, directions):
    global files
    if n_clicks > 0:
        if years and qualifications and directions:
            data = asyncio.run(get_univeris_data(years, qualifications, directions))
            files[JOURNALS_FILE_NAME], files[STUDENTS_FILE_NAME], files[GRADES_FILE_NAME], files[RATINGS_FILE_NAME], files[EGE_FILE_NAME] = data
            return html.Div("Данные успешно получены")
        else: 
            return html.Div("Ошибка получения данных. Проверьте, заполнены ли все поля")


@app.callback(Output('download-data-zip', 'data'),
              Input('download-data-button', 'n_clicks'),
              State('filename-input', 'value'))
def download_archive_data(n_clicks, filename):
    if n_clicks > 0 and filename and filename != "":
        _, missing_files = check_data_files()
        if len(missing_files) == 0:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zf:
                zf.writestr(JOURNALS_FILE_NAME, files[JOURNALS_FILE_NAME].to_json())
                zf.writestr(STUDENTS_FILE_NAME, files[STUDENTS_FILE_NAME].to_json())
                zf.writestr(GRADES_FILE_NAME, files[GRADES_FILE_NAME].to_json())
                zf.writestr(RATINGS_FILE_NAME, files[RATINGS_FILE_NAME].to_json())
                zf.writestr(EGE_FILE_NAME, files[EGE_FILE_NAME].to_json())
            zip_data = zip_buffer.getvalue()
            return dcc.send_bytes(zip_data, filename=filename + ".zip", mimetype='application/zip')


if __name__ == '__main__':
    app.run_server(debug=True)