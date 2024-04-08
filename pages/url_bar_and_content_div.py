from common_imports import *


url_bar_and_content_div = html.Div([
    html.Div(style={'font-size': '24px'},
            children=[
                html.Div(
                    style={'display': 'flex', 'justify-content': 'center'},
                    children=[
                        dcc.Link('Получение данных', 
                                 href='/get-data', 
                                 style={'margin': '10px', 
                                        'text-decoration': 'none', 
                                        'color': '#333', 
                                        'padding': '10px 20px'}),
                        dcc.Link('Поиск шаблонов', 
                                 href='/find-patterns', 
                                 style={'margin': '10px', 
                                        'text-decoration': 'none', 
                                        'color': '#333', 
                                        'padding': '10px 20px'}),
                    ]
                )
            ]
        ),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])