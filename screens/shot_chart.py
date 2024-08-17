import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

from data.fetch_data import fetch_shot_data, get_player_options


def shot_chart_layout():
    player_options = get_player_options()
    layout = html.Div(
        [
            html.H1("Shot Chart Analysis"),
            dcc.Dropdown(
                id="player-dropdown",
                options=player_options,
                placeholder="Select Player",
            ),
            dcc.Dropdown(
                id="season-dropdown",
                options=[
                    {"label": season, "value": season}
                    for season in ["2023-24", "2022-23", "2021-22"]
                ],
                placeholder="Select Season",
            ),
            html.Div(
                [
                    dcc.Input(
                        id="new-season-input", type="text", placeholder="Add New Season"
                    ),
                    html.Button("Add Season", id="add-season-button", n_clicks=0),
                ],
                style={"display": "flex", "alignItems": "center"},
            ),
            dcc.Dropdown(
                id="game-dropdown",
                placeholder="Select Game",
            ),
            dcc.Graph(id="shot-chart"),
            dcc.Graph(id="shot-heatmap"),
        ]
    )
    return layout
