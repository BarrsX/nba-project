from dash import dcc
from dash import html
import plotly.express as px
from data.fetch_data import get_player_options
from scipy.spatial.distance import euclidean


def calculate_similarity(player1_stats, player2_stats):
    # Select the common metrics for comparison
    metrics = ["PTS", "REB", "AST", "STL", "BLK", "TOV"]

    # Calculate mean per game stats for each player
    player1_mean_stats = player1_stats[metrics].mean()
    player2_mean_stats = player2_stats[metrics].mean()

    # Calculate the Euclidean distance between the players
    distance = euclidean(player1_mean_stats, player2_mean_stats)

    # Calculate similarity as a percentile
    max_distance = euclidean(
        [0] * len(metrics), [30] * len(metrics)
    )  # Assuming max values for metrics
    similarity_percentile = (1 - distance / max_distance) * 100

    return similarity_percentile, player1_mean_stats, player2_mean_stats


def player_similarity_layout():
    player_options = get_player_options()
    layout = html.Div(
        [
            html.H1("Player Similarity Analysis"),
            dcc.Dropdown(
                id="player1_name", options=player_options, placeholder="Select Player 1"
            ),
            dcc.Dropdown(
                id="player2_name", options=player_options, placeholder="Select Player 2"
            ),
            html.Button(id="submit-button", n_clicks=0, children="Compare"),
            html.Div(id="similarity-output"),
            dcc.Graph(id="similarity-graph"),
        ]
    )
    return layout
