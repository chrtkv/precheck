import get_mail
import re

from bs4 import BeautifulSoup

# format text
body_readable = BeautifulSoup(get_mail.main(), features='html5lib')
# convert to string
body_string = str(body_readable)

# convert text to list. Each element is the one tournament description
list_for_parsing = re.split(r"\n[0-9]", body_string)
list_of_tournaments = []
for element in list_for_parsing:
    if "NOTES:" in element:
        list_of_tournaments.append(element)

tournaments_data = []

for element in list_of_tournaments:

    tournament_info_as_list = re.split(r"\n", element)
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



    tournaments_data[list_of_tournaments.index(element)].update({'tour_code': tour_code_variable}) 
    tournaments_data[list_of_tournaments.index(element)].update({'tour_id': tour_id_variable})
    tournaments_data[list_of_tournaments.index(element)].update({'score_type': score_type_variable})
    tournaments_data[list_of_tournaments.index(element)].update({'time_zone': time_zone_variable})
    tournaments_data[list_of_tournaments.index(element)].update({'link': link_variable})

for i in tournaments_data:
    print(i
    )