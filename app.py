import dash
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
from dash import html
from dash.dependencies import Input, Output, State

from data.fetch_data import (
    fetch_players_career_stats,
    get_player_options,
    fetch_team_performance_data,
)
from screens.player_similarity import calculate_similarity, player_similarity_layout
from screens.team_performance import team_performance_layout

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(
    [
        dcc.Tabs(
            id="tabs",
            value="tab-1",
            children=[
                dcc.Tab(label="Team Performance", value="tab-1"),
                dcc.Tab(label="Player Similarity", value="tab-2"),
                # Add more tabs here for other screens
            ],
        ),
        html.Div(id="tabs-content"),
    ]
)


@app.callback(
    Output("tabs-content", "children"),
    Input("tabs", "value"),
)
def render_content(tab):
    if tab == "tab-1":
        return team_performance_layout()
    elif tab == "tab-2":
        return player_similarity_layout()


@app.callback(
    Output("season-dropdown", "options"),
    [Input("add-season-button", "n_clicks")],
    [State("new-season-input", "value"), State("season-dropdown", "options")],
)
def update_season_options(n_clicks, new_season, options):
    if n_clicks > 0 and new_season:
        if {"label": new_season, "value": new_season} not in options:
            options.append({"label": new_season, "value": new_season})
    return options


@app.callback(
    Output("team-performance-graph", "figure"),
    [Input("season-dropdown", "value")],
)
def update_team_performance_graph(selected_seasons):
    if not selected_seasons:
        return px.scatter()  # Return an empty figure if no seasons are selected

    data = fetch_team_performance_data(selected_seasons)
    fig = px.scatter(
        data, x="WINS", y="LOSSES", color="cluster", hover_data=["TEAM_ID", "TEAM_NAME"]
    )
    return fig


@app.callback(
    [Output("similarity-output", "children"), Output("similarity-graph", "figure")],
    [Input("submit-button", "n_clicks")],
    [Input("player1_name", "value"), Input("player2_name", "value")],
)
def update_similarity(n_clicks, player1_id, player2_id):
    if not player1_id or not player2_id:
        return "Please select both players", {}

    player1_stats, player2_stats = fetch_players_career_stats(player1_id, player2_id)
    similarity_percentile, player1_mean_stats, player2_mean_stats = (
        calculate_similarity(player1_stats, player2_stats)
    )

    # Get player names
    player_options = get_player_options()
    player1_name = next(
        item["label"] for item in player_options if item["value"] == player1_id
    )
    player2_name = next(
        item["label"] for item in player_options if item["value"] == player2_id
    )

    # Create a DataFrame for visualization
    data = pd.DataFrame(
        {
            "Metric": player1_mean_stats.index,
            player1_name: player1_mean_stats.values,
            player2_name: player2_mean_stats.values,
        }
    )

    fig = px.bar(data, x="Metric", y=[player1_name, player2_name], barmode="group")

    similarity_output = f"Player Similarity: {similarity_percentile:.2f}%"
    return similarity_output, fig


if __name__ == "__main__":
    app.run_server(debug=True)
