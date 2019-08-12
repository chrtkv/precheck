#!/usr/bin/env python3

import random
import requests
import re

def main(tour_code, tour_number):
    request_template = 'https://statdata.pgatour.com/{}/{}/leaderboard-v2.json'
    leaderboard_raw = requests.get(request_template.format(tour_code, tour_number))
    leaderboard_full = leaderboard_raw.json() #dict
    leaderboard_leaderboard = leaderboard_full.get("leaderboard")
    leaderboard_players = leaderboard_leaderboard.get("players") #list

    def get_players_list(tournament_leaderboard):
        """Get top-5 and 5 random players from leaderboard"""

        players_list = []

        template = 'https://www.pgatour.com/players/player.{}.{}.html'
        random_player_number = random.sample(range(5, 20), 5)
        i = 0

        while i < 20:
            if i in range(5) or i in random_player_number:
                player_id = tournament_leaderboard[i]["player_id"]
                first_name = tournament_leaderboard[i]["player_bio"]["first_name"]
                last_name = tournament_leaderboard[i]["player_bio"]["last_name"]
                full_name = "{}.{}".format(first_name, last_name)

                # doesn't work if whitespace is both in first and last name or more than one whitespace in name
                if ' ' in first_name:
                    first_name = re.split(' ', first_name)
                    full_name = "{}-{}-{}".format(first_name[0], first_name[1], last_name)
                elif ' ' in last_name:
                    last_name = re.split(" ", last_name)
                    full_name = "{}-{}-{}".format(first_name, last_name[0], last_name[1])
                elif '.' in first_name:
                    first_name = re.split('\.', first_name)
                    full_name = "{}-{}--{}".format(first_name[0], first_name[1], last_name)

                players_list.append(template.format(player_id, full_name.lower()))
            i += 1

        return players_list

    return get_players_list(leaderboard_players)

#print(main('r', 028))
