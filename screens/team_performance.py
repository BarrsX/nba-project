import dash_core_components as dcc
import plotly.express as px
from dash import html

from data.fetch_data import fetch_team_performance_data


def team_performance_layout():
    layout = html.Div(
        [
            html.H1("Team Performance Analysis"),
            dcc.Dropdown(
                id="season-dropdown",
                options=[
                    {"label": season, "value": season}
                    for season in ["2023-24", "2022-23", "2021-22"]
                ],
                multi=True,
                searchable=True,
                placeholder="Select or type a season",
            ),
            dcc.Input(
                id="new-season-input",
                type="text",
                placeholder="Enter new season (e.g., 2024-25)",
            ),
            html.Button("Add Season", id="add-season-button", n_clicks=0),
            dcc.Graph(id="team-performance-graph"),
        ]
    )
    return layout
