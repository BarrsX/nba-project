from nba_api.stats.endpoints import (
    leaguegamefinder,
    playercareerstats,
    leaguedashplayerstats,
)
from nba_api.stats.static import teams
from nba_api.stats.static import players

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd


def fetch_team_performance_data(seasons=["2023-24"]):
    print("Fetching team performance data for seasons:", seasons)
    all_games = []

    for season in seasons:
        gamefinder = leaguegamefinder.LeagueGameFinder(
            season_nullable=season, season_type_nullable="Regular Season"
        )
        games = gamefinder.get_data_frames()[0]
        all_games.append(games)

    games = pd.concat(all_games, ignore_index=True)

    # Existing code to process games data
    nba_teams = teams.get_teams()
    nba_team_ids = [team["id"] for team in nba_teams]
    games = games[games["TEAM_ID"].isin(nba_team_ids)]
    team_wins = (
        games[games["WL"] == "W"].groupby("TEAM_ID").size().reset_index(name="WINS")
    )
    team_losses = (
        games[games["WL"] == "L"].groupby("TEAM_ID").size().reset_index(name="LOSSES")
    )
    team_wl = pd.merge(team_wins, team_losses, on="TEAM_ID", how="outer").fillna(0)
    numeric_cols = games.select_dtypes(include=["number"]).columns
    team_stats_numeric = (
        games.groupby("TEAM_ID")[numeric_cols]
        .mean()
        .rename(columns={"TEAM_ID": "T_ID"})
    )
    team_names = games[["TEAM_ID", "TEAM_NAME"]].drop_duplicates()
    assert team_names[
        "TEAM_ID"
    ].is_unique, "Duplicate TEAM_ID entries found in team_names DataFrame"
    team_stats = pd.merge(team_stats_numeric, team_names, on="TEAM_ID", how="left")
    team_stats = pd.merge(team_stats, team_wl, on="TEAM_ID", how="left")

    features = [
        "FGM",
        "FGA",
        "FG_PCT",
        "FG3M",
        "FG3A",
        "FG3_PCT",
        "FTM",
        "FTA",
        "FT_PCT",
        "OREB",
        "DREB",
        "REB",
        "AST",
        "STL",
        "BLK",
        "TOV",
    ]
    if not all(feature in team_stats.columns for feature in features):
        missing_features = [
            feature for feature in features if feature not in team_stats.columns
        ]
        raise ValueError(
            f"Missing required features for clustering: {missing_features}"
        )

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(team_stats[features])
    kmeans = KMeans(n_clusters=5, random_state=42)
    team_stats["cluster"] = kmeans.fit_predict(scaled_features)

    return team_stats


def fetch_player_career_stats(player_id):
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_stats = career.get_data_frames()[0]

    # Calculate per game stats
    per_game_stats = career_stats.copy()
    per_game_stats["PTS"] = per_game_stats["PTS"] / per_game_stats["GP"]
    per_game_stats["REB"] = per_game_stats["REB"] / per_game_stats["GP"]
    per_game_stats["AST"] = per_game_stats["AST"] / per_game_stats["GP"]
    per_game_stats["STL"] = per_game_stats["STL"] / per_game_stats["GP"]
    per_game_stats["BLK"] = per_game_stats["BLK"] / per_game_stats["GP"]
    per_game_stats["TOV"] = per_game_stats["TOV"] / per_game_stats["GP"]

    return per_game_stats


def fetch_players_career_stats(player1_id, player2_id):
    player1_stats = fetch_player_career_stats(player1_id)
    player2_stats = fetch_player_career_stats(player2_id)
    return player1_stats, player2_stats


def get_player_options():
    player_data = players.get_players()
    options = [
        {"label": player["full_name"], "value": player["id"]} for player in player_data
    ]
    return options


def fetch_league_player_stats(season="2023-24"):
    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season)
    return player_stats.get_data_frames()[0]
