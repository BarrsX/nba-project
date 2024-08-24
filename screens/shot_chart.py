import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

from data.fetch_data import fetch_shot_data, get_player_options


def shot_chart_layout():
    player_options = get_player_options()
    layout = html.Div(
        [
            html.H1("Shot Chart Analysis", style={"textAlign": "center"}),
            html.Div(
                [
                    dcc.Dropdown(
                        id="player-dropdown",
                        options=player_options,
                        placeholder="Select Player",
                        style={
                            "width": "30%",
                            "display": "inline-block",
                            "marginRight": "10px",
                        },
                    ),
                    dcc.Dropdown(
                        id="season-dropdown",
                        options=[
                            {"label": season, "value": season}
                            for season in ["2023-24", "2022-23", "2021-22"]
                        ],
                        placeholder="Select Season",
                        style={
                            "width": "30%",
                            "display": "inline-block",
                            "marginRight": "10px",
                        },
                    ),
                    dcc.Dropdown(
                        id="game-dropdown",
                        placeholder="Select Game",
                        style={"width": "30%", "display": "inline-block"},
                    ),
                ],
                style={"textAlign": "center", "marginBottom": "20px"},
            ),
            html.Div(
                [dcc.Graph(id="shot-chart", style={"height": "80vh"})],
                style={"width": "100%", "display": "flex", "justifyContent": "center"},
            ),
        ]
    )
    return layout
