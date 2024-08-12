import dash_core_components as dcc
from dash import html
import plotly.express as px
from data.fetch_data import fetch_player_career_stats


def player_similarity_layout(player_id):
    data = fetch_player_career_stats(player_id)
    fig = px.scatter(data, x="PTS", y="REB", color="SEASON_ID")
    layout = html.Div([html.H1("Player Similarity Analysis"), dcc.Graph(figure=fig)])
    return layout
