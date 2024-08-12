import dash_core_components as dcc
from dash import html
import plotly.express as px
from data.fetch_data import fetch_team_performance_data


def team_performance_layout():
    data = fetch_team_performance_data()
    fig = px.scatter(
        data, x="WINS", y="LOSSES", color="cluster", hover_data=["TEAM_ID", "TEAM_NAME"]
    )
    layout = html.Div([html.H1("Team Performance Analysis"), dcc.Graph(figure=fig)])
    return layout
