#!/usr/bin/env python3

import random
import requests

leaderboard_raw = requests.get('http://statdata.pgatour.com/r/027/leaderboard-v2.json')
leaderboard_full = leaderboard_raw.json() #dict
leaderboard_leaderboard = leaderboard_full.get("leaderboard")
leaderboard_players = leaderboard_leaderboard.get("players") #list

def get_players_list(tournament_leaderboard):
    """Get top-5 and 5 random players from leaderboard"""
    template = 'https://www.pgatour.com/players/player.{}.{}.{}.html'
    random_player_number = random.sample(range(5, 20), 5)
    i = 0

    while i < 20:
        if i in range(5) or i in random_player_number:
            player_id = tournament_leaderboard[i]["player_id"]
            first_name = tournament_leaderboard[i]["player_bio"]["first_name"]
            last_name = tournament_leaderboard[i]["player_bio"]["last_name"]
            print(template.format(player_id, first_name.lower(), last_name.lower()))
        i += 1
print(leaderboard_players)
#get_players_list(leaderboard_players)
