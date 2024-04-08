from common_imports import *


layout_get_data_page = html.Div([
    html.Div(
        style={'display': 'flex', 
               'flex-direction': 'column', 
               'align-items': 'center', 
               'padding': '20px'},
        children=[
            html.Div(
                children=[
                    html.Label('Выберите года:'),
                    dcc.Dropdown(
                        id='year-dropdown',
                        multi=True,
                        optionHeight=50,
                        style={'width': '500px', 'maxWidth': '500px'}
                    )
                ],
                style={'margin-bottom': '20px'}
            ),
            html.Div(
                children=[
                    html.Label('Выберите квалификации:'),
                    dcc.Dropdown(
                        id='qualification-dropdown', 
                        multi=True,
                        optionHeight=50,
                        style={'width': '500px', 'maxWidth': '500px'}
                    )
                ],
                style={'margin-bottom': '20px'}
            ),
            html.Div(
                children=[
                    html.Label('Выберите специальности:'),
                    dcc.Dropdown(
                        id='directions-dropdown',
                        multi=True,
                        optionHeight=50,
                        style={'width': '500px', 'maxWidth': '500px'}
                    )
                ],
                style={'margin-bottom': '20px'},
            ),
            html.Div([
                html.Button('Получить данные', 
                    id='get-data-btn', 
                    n_clicks=0,
                    style={'height': '50px', 'width': '500px'}),
                html.Div(id='output-get-data-btn'),
                dcc.Store(id='warning-message', storage_type='session')
                ],
                style={'margin-bottom': '20px'}
            ),  
            dcc.Store(id='store', 
                      storage_type='session'),
            html.Div(
                style={'display': 'flex', 
                       'justify-content': 'space-between', 
                       'margin-top': '10px'},
                children=[
                    html.Div(
                        children=[
                            html.Label('Скачать архив с именем:'),
                            dcc.Input(
                                id='filename-input', 
                                type='text', 
                                value='data', 
                                style={'width': '280px'},
                                required=True),
                        ],
                        style={'margin-left': '10px'}
                    ),
                    html.Div([
                        html.Button('Скачать данные', 
                            id="download-data-button", 
                            n_clicks=0, 
                            style={'height': '50px', 'width': '200px'}),
                        dcc.Download(id="download-data-zip"),
                    ], style={'display': 'flex', 
                              'flex-direction': 'column', 
                              'margin': '12px', 
                              'margin-left': '20px'}
                    )
                ]
            ),
        ]
    ),
])