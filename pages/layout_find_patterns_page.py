from common_imports import *


layout_find_patterns_page = html.Div(
    children=[
        html.Div(
            style={'display': 'flex', 
                   'flex-direction': 'column', 
                   'align-items': 'center', 
                   'padding': '20px'},
            children=[
                html.Div([
                    html.Label('Загрузить данные:'),
                    dcc.Upload(
                        id="upload-json-data",
                        children=html.Div([
                            'Перетащите или ',
                            html.A('выберите файл')
                        ]),
                        style={
                            'width': '500px',
                            'height': '50px',
                            'line-height': '50px',
                            'border-width': '1px',
                            'border-style': 'dashed',
                            'border-radius': '5px',
                            'text-align': 'center',
                        },
                        multiple=True
                    ),
                ]),
            ]
        ),
        html.Div(
            style={'display': 'flex', 
                   'flex-direction': 'column', 
                   'align-items': 'center', 
                   'margin-right': '10px'},
            children=[
                html.Div(id='output-upload-json-data', 
                         style={'width': '490px'}),
            ]),
        html.Div(
            style={'display': 'flex', 
                   'flex-direction': 'column', 
                   'align-items': 'center', 
                   'padding': '10px'},
            children=[
                html.Div(style={'display': 'flex', 
                                'justify-content': 'center', 
                                'flex-direction': 'column'}, 
                        children=[
                            html.Div([
                                html.Label('Введите поддержку:'),
                                dcc.Input(id='sup', 
                                          type='number', 
                                          value=0.1, 
                                          min=0, 
                                          step=0.01, 
                                          style={'width': '500px'},
                                          required=True),
                            ], style={'margin': '10px'}),
                            html.Div([
                                html.Label('Введите достоверность:'),
                                dcc.Input(id='conf', 
                                          type='number',
                                          value=0.1, 
                                          min=0, 
                                          step=0.1, 
                                          style={'width': '500px'},
                                          required=True),
                            ], style={'margin': '10px'}),
                            html.Div([
                                html.Label('Введите подъем:'),
                                dcc.Input(id='lift', 
                                          type='number', 
                                          value=1, 
                                          min=0, 
                                          step=0.1, 
                                          style={'width': '500px'},
                                          required=True),
                            ], style={'margin': '10px'}),
                            html.Div([
                                html.Label('Максимум элементов слева:'),
                                dcc.Input(id='left_el', 
                                          type='number', 
                                          value=3, 
                                          min=1, 
                                          step=1, style={'width': '500px'},
                                    required=True),
                            ], style={'margin': '10px'}),
                            html.Div([
                                html.Label('Максимум элементов справа:'),
                                dcc.Input(id='right_el', 
                                          type='number', 
                                          value=1, 
                                          min=1, 
                                          step=1, 
                                          style={'width': '500px'},
                                          required=True),
                            ], style={'margin': '10px'}),
                            html.Div([
                                    html.Button('Выполнить поиск', 
                                                id='search-btn', 
                                                n_clicks=0, 
                                                style={'width': '500px', 
                                                       'height': '50px', 
                                                       'font-size': '12px'}),
                                    ],
                                    style={"margin-left":"10px", 
                                           'margin': '10px'}
                                ),
                        ],
                ),
                html.Div(
                    style={'display': 'flex', 
                           'flex-direction': 'column', 
                           'align-items': 'center'},
                    children=[
                        html.Div(
                            style={'display': 'flex', 
                                   'justify-content': 'space-between', 
                                   'margin-top': '10px'},
                            children=[
                                html.Div(
                                    children=[
                                        html.Label('Имя файла:'),
                                        dcc.Input(
                                            id='excel-filename-input', 
                                            type='text', 
                                            value='Шаблоны', 
                                            style={'width': '290px'},
                                            required=True
                                            ),
                                    ],
                                    style={'margin-left': '10px'}
                                ),
                                html.Div([
                                    html.Button('Скачать шаблоны', 
                                                id="export-btn", 
                                                n_clicks=0, 
                                                style={'height': '50px'}),
                                    html.Div(id="output-export-btn"),
                                    dcc.Download(id="download-dataframe-xlsx"),
                                ], style={'display': 'flex', 
                                          'flex-direction': 'column', 
                                          'margin': "10px", 
                                          'margin-left': '20px'})
                            ]
                        ),
                    ]
                ),
                html.Div(
                    style={'display': 'flex', 
                           'flex-direction': 'column', 
                           'align-items': 'center'},
                    children=[
                        html.Div(id='output-search-btn',
                                 style={'text-align': 'center', 
                                        "margin": "20px"})
                    ]
                )
            ]
        )
    ],
)