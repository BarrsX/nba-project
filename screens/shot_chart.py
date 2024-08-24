import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

from data.fetch_data import fetch_shot_data, get_player_options


def shot_chart_layout():
    player_options = get_player_options()
    layout = html.Div(
        [
            html.H1("Shot Chart Analysis", className="text-center"),
            html.Div(
                [
                    dcc.Dropdown(
                        id="player-dropdown",
                        options=player_options,
                        placeholder="Select Player",
                        className="input-element",
                    ),
                    dcc.Dropdown(
                        id="season-dropdown",
                        options=[
                            {"label": season, "value": season}
                            for season in ["2023-24", "2022-23", "2021-22"]
                        ],
                        placeholder="Select Season",
                        className="input-element",
                    ),
                    dcc.Input(
                        id="new-season-input",
                        type="text",
                        placeholder="Enter new season (e.g., 2024-25)",
                        className="input-element",
                    ),
                    html.Button(
                        "Add Season",
                        id="add-season-button",
                        n_clicks=0,
                        className="input-element",
                    ),
                ],
                className="input-container",
            ),
            dcc.Dropdown(
                id="game-dropdown",
                placeholder="Select Game",
                className="game-dropdown",
            ),
            html.Div(
                [dcc.Graph(id="shot-chart", className="shot-chart-graph")],
                className="chart-container",
            ),
        ]
    )
    return layout
