"""Generates list of tournaments.
Each tournament is dict element of the list.
Contains all data needed for filling spreadsheet"""
import re

from bs4 import BeautifulSoup

import get_mail


def genetate_list_of_tours(email_text):
    """Generate list of tours from email text."""
    list_of_tours = []
    # format text
    body_readable = BeautifulSoup(email_text, features='html5lib')
    # convert to string
    body_string = str(body_readable)

    # convert text to list.
    list_for_parsing = re.split(r"\n[0-9]", body_string)
    # Filter list to find only tour info. Each element is the one tournament's description
    for element in list_for_parsing:
        if "NOTES:" in element:
            list_of_tours.append(element)

    return list_of_tours


def main():
    """Parses text and generates list with tours data"""
    tournaments_data = []
    unparsed_list = genetate_list_of_tours(get_mail.main())
    
    for element in unparsed_list:
        # split text to lines
        tournament_info_as_list = re.split(r"\n", element)
        # generate list of dictionaries for each tour
        tournaments_data.append({'name': tournament_info_as_list[1]})

        for element2 in tournament_info_as_list:
            if "korean" in element2.lower():
                tour_code_variable = "R"
            elif "korn" in element2.lower():
                tour_code_variable = "H"
            elif "canada" in element2.lower():
                tour_code_variable = "C"
            elif "/champions/" in element2.lower():
                tour_code_variable = "S"
            elif "latinoamerica" in element2.lower():
                tour_code_variable = "M"

            if "time zone" in element2.lower():
                time_zone_variable = re.split(r": +", element2)[1]
            if "tournament id" in element2.lower():
                tour_id_variable = re.split(r": +", element2)[1]
            if "score type" in element2.lower():
                score_type_variable = re.split(r": +", element2)[1]
            if "LB" in element2:
                link_variable = re.split(r"/", element2)[-2]

        tournaments_data[unparsed_list.index(element)].update({'tour_code': tour_code_variable})
        tournaments_data[unparsed_list.index(element)].update({'tour_id': tour_id_variable})
        tournaments_data[unparsed_list.index(element)].update({'score_type': score_type_variable})
        tournaments_data[unparsed_list.index(element)].update({'time_zone': time_zone_variable})
        tournaments_data[unparsed_list.index(element)].update({'link': link_variable})
        
    return tournaments_data
