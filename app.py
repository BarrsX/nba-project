import dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output

from screens.team_performance import team_performance_layout
from screens.player_similarity import player_similarity_layout

app = dash.Dash(__name__)

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


@app.callback(Output("tabs-content", "children"), Input("tabs", "value"))
def render_content(tab):
    if tab == "tab-1":
        return team_performance_layout()
    elif tab == "tab-2":
        return player_similarity_layout(2544)  # Example player_id for LeBron James


if __name__ == "__main__":
    app.run_server(debug=True)
