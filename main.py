from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from data import (
    countries_df,
    totals_df,
    dropdown_options,
    make_global_df,
    make_country_df,
)
from builders import make_table

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.2/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap",
]

app = Dash(__name__, external_stylesheets=stylesheets)

server = app.server

bubble_map = px.scatter_geo(
    countries_df,
    template="plotly_dark",
    color_continuous_scale=px.colors.sequential.Oryel,
    size="Confirmed",
    title="Confirmed By Country",
    size_max=40,
    locations="Country_Region",
    locationmode="country names",
    color="Confirmed",
    hover_name="Country_Region",
    hover_data={
        "Confirmed": True,
        "Recovered": True,
        "Deaths": True,
        "Country_Region": False,
    },
)
bubble_map.update_layout(margin=dict(l=0, r=0, t=30, b=0))

bars_graph = px.bar(
    totals_df,
    x="condition",
    y="count",
    template="plotly_dark",
    title="Total Global Cases",
    labels={"condition": "Condition", "count": "Count", "color": "Condition"},
)
bars_graph.update_traces(marker_color=["#e74c3c", "#9b59b6", "#27ae60"])

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
    },
    children=[
        html.Header(
            style={
                "textAlign": "center",
                "paddingTop": "50px",
                "fontFamily": "Open Sans",
                "paddingBottom": 50,
            },
            children=[
                html.H1(
                    "Corona Dashboard",
                    style={
                        "fontSize": "40px",
                    },
                ),
            ],
        ),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)"},
            children=[
                html.Div(
                    style={"grid-column": "span 3", "gap": 50},
                    children=[
                        dcc.Graph(
                            figure=bubble_map,
                        ),
                    ],
                ),
                html.Div(
                    children=[make_table(countries_df)],
                ),
            ],
        ),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)"},
            children=[
                html.Div(
                    style={"grid-column": "span 1", "gap": 50},
                    children=[
                        dcc.Graph(
                            figure=bars_graph,
                        ),
                    ],
                ),
                html.Div(
                    style={"grid-column": "span 3", "gap": 50},
                    children=[
                        dcc.Dropdown(
                            style={
                                "width": 320,
                                "margin": "0 auto",
                                "color": "#111111",
                            },
                            id="country",
                            options=[
                                {"label": country, "value": country}
                                for country in dropdown_options
                            ],
                        ),
                        dcc.Graph(id="country_graph"),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(Output("country_graph", "figure"), [Input("country", "value")])
def update_hello(value):
    if value:
        df = make_country_df(value)
    else:
        df = make_global_df()

    fig = px.line(
        df,
        template="plotly_dark",
        x="date",
        y=["confirmed", "deaths", "recovered"],
        title="Global Conditions",
        labels={"value": "Cases", "variable": "Condition", "date": "Date"},
        hover_data={
            "variable": False,
        },
    )
    fig.update_xaxes(
        rangeslider_visible=True,
    )
    fig["data"][0]["line"]["color"] = "#e74c3c"
    fig["data"][1]["line"]["color"] = "#9b59b6"
    fig["data"][2]["line"]["color"] = "#27ae60"
    return fig


if __name__ == "__main__":
    app.run(debug=True)
