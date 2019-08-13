#!/usr/bin/env python3

import random
import requests
import re
from datetime import datetime
import sys

def main(tour_code, tour_number):
    request_template = 'https://statdata.pgatour.com/{}/{}/leaderboard-v2.json'
    leaderboard_raw = requests.get(request_template.format(tour_code, tour_number))
    leaderboard_full = leaderboard_raw.json() #dict
    leaderboard_leaderboard = leaderboard_full.get("leaderboard")
    leaderboard_players = leaderboard_leaderboard.get("players") #list
    
    current_year = str(datetime.now().year)

    def is_tour_info_actual(current_year):
        """Recieves current year. Returns True if json actual or False if not"""
        leaderboard_debug = leaderboard_full.get("debug")
        tour_year = leaderboard_debug['setup_year']

        return current_year == tour_year

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
                    last_name = re.split(' ', last_name)
                    full_name = "{}-{}-{}".format(first_name, last_name[0], last_name[1])
                elif '.' in first_name:
                    first_name = re.split('\.', first_name)
                    full_name = "{}-{}--{}".format(first_name[0], first_name[1], last_name)

                players_list.append(template.format(player_id, full_name.lower()))
            i += 1

        return players_list

    if is_tour_info_actual(current_year):
        return get_players_list(leaderboard_players)
    else:
        placeholder = []
        i = 0
        while i < 10:
            placeholder.append("Fill it by hand when tour will be live or use './players_list.py TOUR_CODE TOUR_ID' for generating a list")
            i += 1
        if __name__ == '__main__':
            placeholder = 'Tour is not live. Try again later'
        return(placeholder) 

if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] in ["--help", "-h", "help"]:
        print("Usage: players_list.py code(R, S, H, C) id(3 digits)\n\nPrint top-5 players on the top and 5 random players below")
    else:
        if "Try again" in main(sys.argv[1], sys.argv[2]):
            print(main(sys.argv[1], sys.argv[2]))
        else:
            for i in main(sys.argv[1], sys.argv[2]):
                print(i)