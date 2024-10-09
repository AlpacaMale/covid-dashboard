from dash import html


def make_table(df):
    return html.Table(
        children=[
            html.Thead(
                children=[
                    html.Tr(
                        children=[
                            html.Th(column_name.replace("_", " "))
                            for column_name in df.columns
                        ],
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4, 1fr)",
                            "fontWeight": "600",
                            "fontSize": 22,
                        },
                    )
                ],
                style={
                    "display": "block",
                    "marginBottom": 25,
                },
            ),
            html.Tbody(
                children=[
                    html.Tr(
                        children=[html.Td(value_column) for value_column in value],
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4, 1fr)",
                            "border-top": "1px solid white",
                            "padding": "30px 0px",
                            "textAlign": "center",
                        },
                    )
                    for value in df.values
                ],
                style={
                    "maxHeight": "50vh",
                    "overflow": "scroll",
                    "display": "block",
                },
            ),
        ],
        style={
            # 스크롤바를 숨기기 위한 CSS
            "scrollbarWidth": "none",  # Firefox에서 스크롤바 숨기기
        },
    )
