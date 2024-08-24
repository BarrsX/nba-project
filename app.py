import os

import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output, State

from data.fetch_data import (
    fetch_game_options,
    fetch_players_career_stats,
    fetch_shot_data,
    fetch_team_performance_data,
    get_player_options,
)
from screens.player_similarity import calculate_similarity, player_similarity_layout
from screens.shot_chart import shot_chart_layout
from screens.team_performance import team_performance_layout

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(
    [
        dcc.Tabs(
            id="tabs",
            value="tab-1",
            children=[
                dcc.Tab(label="Team Performance", value="tab-1", className="tab-label"),
                dcc.Tab(
                    label="Player Similarity", value="tab-2", className="tab-label"
                ),
                dcc.Tab(
                    label="Shot Chart Analysis", value="tab-3", className="tab-label"
                ),
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
    elif tab == "tab-3":
        return shot_chart_layout()


@app.callback(
    [
        Output("shot-chart", "figure"),
        Output("game-dropdown", "options"),
        Output("season-dropdown", "options"),
    ],
    [
        Input("tabs", "value"),
        Input("player-dropdown", "value"),
        Input("season-dropdown", "value"),
        Input("game-dropdown", "value"),
        Input("add-season-button", "n_clicks"),
    ],
    [
        State("new-season-input", "value"),
        State("season-dropdown", "options"),
    ],
)
def update_shot_charts_and_seasons(
    active_tab, player_id, season, game_id, n_clicks, new_season, season_options
):
    if active_tab != "tab-3":  # Only update when Shot Chart tab is active
        return dash.no_update, dash.no_update, dash.no_update

    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Handle adding new season
    if triggered_id == "add-season-button" and new_season:
        if {"label": new_season, "value": new_season} not in season_options:
            season_options.append({"label": new_season, "value": new_season})
        return dash.no_update, dash.no_update, season_options

    # Handle updating shot chart
    if not player_id or not season:
        return px.scatter(), [], season_options

    game_options = fetch_game_options(player_id, season)

    if not game_id:
        return px.scatter(), game_options, season_options

    shot_data = fetch_shot_data(player_id, season, game_id)

    shot_chart = go.Figure()

    # Add court image
    shot_chart.add_layout_image(
        dict(
            source=app.get_asset_url("shot_chart.png"),
            xref="x",
            yref="y",
            x=-250,
            y=422.5,
            sizex=500,
            sizey=470,
            sizing="stretch",
            opacity=1,
            layer="below",
        )
    )

    # Add made shots
    shot_chart.add_trace(
        go.Scatter(
            x=shot_data[shot_data["SHOT_MADE_FLAG"] == 1]["LOC_X"],
            y=shot_data[shot_data["SHOT_MADE_FLAG"] == 1]["LOC_Y"],
            mode="markers",
            marker=dict(size=8, color="green", symbol="circle"),
            name="Made Shot",
            text="Made Shot",
            hoverinfo="text",
        )
    )

    # Add missed shots
    shot_chart.add_trace(
        go.Scatter(
            x=shot_data[shot_data["SHOT_MADE_FLAG"] == 0]["LOC_X"],
            y=shot_data[shot_data["SHOT_MADE_FLAG"] == 0]["LOC_Y"],
            mode="markers",
            marker=dict(size=8, color="red", symbol="x"),
            name="Missed Shot",
            text="Missed Shot",
            hoverinfo="text",
        )
    )

    # Update layout
    shot_chart.update_layout(
        title="Shot Chart",
        xaxis=dict(range=[-250, 250], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-52, 422.5], showgrid=False, zeroline=False, visible=False),
        yaxis_scaleanchor="x",
        yaxis_scaleratio=1,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        width=600,
        height=564,
        margin=dict(l=0, r=100, t=30, b=0),
        legend=dict(
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.05,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="rgba(0, 0, 0, 0.3)",
            borderwidth=1,
        ),
        legend_title_text="Shot Outcome",
    )

    return shot_chart, game_options, season_options


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
