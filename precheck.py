#!/usr/bin/env python3
"""
This module creates a spreadsheet from the template,
shares it, fills it from the schedule email and returns link to the spreadsheet.
"""

import json

import gspread
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

import delete_template_worksheets
import get_current_year_for_tour
import players_list
from generate_tours_list import main as generate_tours_list
from precheck_date import main as precheck_date

# load templates
with open('templates/tournaments.json') as template_data:
    TEMPLATE = json.load(template_data)
TEMPLATE_R = TEMPLATE['r']
TEMPLATE_S = TEMPLATE['s']
TEMPLATE_H = TEMPLATE['h']
TEMPLATE_C = TEMPLATE['c']
TEMPLATE_M = TEMPLATE['m']

# load config
with open('config.json') as config_data:
    CONFIG = json.load(config_data)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
KEYFILE_NAME = CONFIG['google']['keyfile']

CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(KEYFILE_NAME, SCOPES)
TEMPLATE_ID = CONFIG['spreadsheet']['template_id']
SHARE_EMAILS = CONFIG['spreadsheet']['share']
SHEET_NAME_TEMPLATE = CONFIG['spreadsheet']['name']
SHEET_NAME = SHEET_NAME_TEMPLATE.format(precheck_date())
TOURS_LIST = generate_tours_list()


def create_spreadsheet():
    """Copies spreadsheet from template and shares it with users"""
    google_sheet = gspread.authorize(CREDENTIALS)
    # Copy spreadsheet from template and share it
    sheet = google_sheet.copy(TEMPLATE_ID, title=SHEET_NAME, copy_permissions=True)
    sheet.share(SHARE_EMAILS, perm_type='user', role='writer', notify=False)

    return sheet


def get_actual_template_worksheet_index(tour_code, sheet_id):
    """Returns actual index of worksheet with template for appropriate tour"""
    list_of_worksheets = []
    list_of_indexes = {}
    spreadsheet = discovery.build('sheets', 'v4', credentials=CREDENTIALS)
    request = spreadsheet.spreadsheets().get(spreadsheetId=sheet_id, includeGridData=False)
    response = request.execute()

    for i in response['sheets']:
        list_of_worksheets.append(i['properties'])

    for i in list_of_worksheets:
        if i['title'] == 'PGA TOUR':
            list_of_indexes.update({'R': i['index']})
        elif i['title'] == 'Korn Ferry':
            list_of_indexes.update({'H': i['index']})
        elif i['title'] == 'Mackenzie-Canada':
            list_of_indexes.update({'C': i['index']})
        elif i['title'] == 'Champions':
            list_of_indexes.update({'S': i['index']})
        elif i['title'] == 'Latinoamerica':
            list_of_indexes.update({'M': i['index']})

    index = list_of_indexes[tour_code]

    return index


def fill_spreadsheet(tours, sheet):
    """Fills spreadsheet"""
    sheet_id = sheet.id

    for element in tours:
        if element["tour_code"] == 'R':
            pga_name = element['name']
            pga_code = element['tour_code']
            pga_id = element['tour_id']
            pga_score = element['score_type']
            pga_time = element['time_zone']
            pga_link = element['link']
            pga_year = get_current_year_for_tour.main(pga_code)
            pga_players = players_list.main(pga_code.lower(), pga_id)
            worksheet_index = get_actual_template_worksheet_index(pga_code, sheet_id)
            worksheet = sheet.get_worksheet(worksheet_index)
            ws_new = worksheet.duplicate(new_sheet_name=pga_name, insert_sheet_index=1)

            # Fill cells
            ws_new.update_acell(TEMPLATE_R['description']['cell'],
                                TEMPLATE_R['description']['templ'].format(pga_name, pga_code, pga_id, pga_time, pga_score))
            ws_new.update_acell(TEMPLATE_R['homepage']['cell'], TEMPLATE_R['homepage']['templ'].format(pga_link))
            ws_new.update_acell(TEMPLATE_R['field']['cell'], TEMPLATE_R['field']['templ'].format(pga_link))
            ws_new.update_acell(TEMPLATE_R['tee-times']['cell'], TEMPLATE_R['tee-times']['templ'].format(pga_link))
            ws_new.update_acell(TEMPLATE_R['leaderboard']['cell'], TEMPLATE_R['leaderboard']['templ'].format(pga_year, pga_link))
            ws_new.update_acell(TEMPLATE_R['yahoo']['cell'], TEMPLATE_R['yahoo']['templ'].format(pga_year, pga_id))
            ws_new.update_acell(TEMPLATE_R['korean']['cell'], TEMPLATE_R['korean']['templ'].format(pga_year, pga_link))
            ws_new.update_acell(TEMPLATE_R['past-results']['cell'], TEMPLATE_R['past-results']['templ'].format(pga_link))
            ws_new.update_acell(TEMPLATE_R['past-winners']['cell'], TEMPLATE_R['past-winners']['templ'].format(pga_link))
            ws_new.update_acell(TEMPLATE_R['course']['cell'], TEMPLATE_R['course']['templ'].format(pga_link))
            ws_new.update_acell(TEMPLATE_R['weather']['cell'], TEMPLATE_R['weather']['templ'].format(pga_link))
            ws_new.update_acell(TEMPLATE_R['pinsheet']['cell'], TEMPLATE_R['pinsheet']['templ'].format(pga_year, pga_link))

            players_cells = worksheet.range('B32:B41')
            i = 0
            for cell in players_cells:
                cell.value = pga_players[i]
                i += 1
            ws_new.update_cells(players_cells)


        if element["tour_code"] == 'S':
            ch_name = element['name']
            ch_code = element['tour_code']
            ch_id = element['tour_id']
            ch_score = element['score_type']
            ch_time = element['time_zone']
            ch_link = element['link']
            ch_year = get_current_year_for_tour.main(ch_code)
            ch_players = players_list.main(ch_code.lower(), ch_id)
            worksheet_index = get_actual_template_worksheet_index(ch_code, sheet_id)
            worksheet = sheet.get_worksheet(worksheet_index)
            ws_new = worksheet.duplicate(new_sheet_name=ch_name, insert_sheet_index=worksheet_index - 1)

            # Fill cells
            ws_new.update_acell(TEMPLATE_S['description']['cell'],
                                TEMPLATE_S['description']['templ'].format(ch_name, ch_code, ch_id, ch_time, ch_score))
            ws_new.update_acell(TEMPLATE_S['homepage']['cell'], TEMPLATE_S['homepage']['templ'].format(ch_link))
            ws_new.update_acell(TEMPLATE_S['field']['cell'], TEMPLATE_S['field']['templ'].format(ch_link))
            ws_new.update_acell(TEMPLATE_S['tee-times']['cell'], TEMPLATE_S['tee-times']['templ'].format(ch_link))
            ws_new.update_acell(TEMPLATE_S['leaderboard']['cell'], TEMPLATE_S['leaderboard']['templ'].format(ch_year, ch_link))
            ws_new.update_acell(TEMPLATE_S['past-results']['cell'], TEMPLATE_S['past-results']['templ'].format(ch_link))
            ws_new.update_acell(TEMPLATE_S['past-winners']['cell'], TEMPLATE_S['past-winners']['templ'].format(ch_link))
            ws_new.update_acell(TEMPLATE_S['course']['cell'], TEMPLATE_S['course']['templ'].format(ch_link))
            ws_new.update_acell(TEMPLATE_S['weather']['cell'], TEMPLATE_S['weather']['templ'].format(ch_link))

            players_cells = worksheet.range('B21:B30')
            i = 0
            for cell in players_cells:
                cell.value = ch_players[i]
                i += 1
            ws_new.update_cells(players_cells)


        if element["tour_code"] == 'H':
            korn_name = element['name']
            korn_code = element['tour_code']
            korn_id = element['tour_id']
            korn_score = element['score_type']
            korn_time = element['time_zone']
            korn_link = element['link']
            worksheet_index = get_actual_template_worksheet_index(korn_code, sheet_id)
            worksheet = sheet.get_worksheet(worksheet_index)
            ws_new = worksheet.duplicate(new_sheet_name=korn_name, insert_sheet_index=worksheet_index - 1)

            # Fill cells
            ws_new.update_acell(TEMPLATE_H['description']['cell'],
                                TEMPLATE_H['description']['templ'].format(korn_name, korn_code, korn_id, korn_time, korn_score))
            ws_new.update_acell(TEMPLATE_H['homepage']['cell'], TEMPLATE_H['homepage']['templ'].format(korn_link))
            ws_new.update_acell(TEMPLATE_H['field']['cell'], TEMPLATE_H['field']['templ'].format(korn_link))
            ws_new.update_acell(TEMPLATE_H['tee-times']['cell'], TEMPLATE_H['tee-times']['templ'].format(korn_link))
            ws_new.update_acell(TEMPLATE_H['leaderboard']['cell'], TEMPLATE_H['leaderboard']['templ'].format(korn_link))
            ws_new.update_acell(TEMPLATE_H['past-results']['cell'], TEMPLATE_H['past-results']['templ'].format(korn_link))
            ws_new.update_acell(TEMPLATE_H['past-winners']['cell'], TEMPLATE_H['past-winners']['templ'].format(korn_link))
            ws_new.update_acell(TEMPLATE_H['course']['cell'], TEMPLATE_H['course']['templ'].format(korn_link))
            ws_new.update_acell(TEMPLATE_H['weather']['cell'], TEMPLATE_H['weather']['templ'].format(korn_link))

        if element["tour_code"] == 'C':
            can_name = element['name']
            can_code = element['tour_code']
            can_id = element['tour_id']
            can_score = element['score_type']
            can_time = element['time_zone']
            can_link = element['link']
            worksheet_index = get_actual_template_worksheet_index(can_code, sheet_id)
            worksheet = sheet.get_worksheet(worksheet_index)
            ws_new = worksheet.duplicate(new_sheet_name=can_name, insert_sheet_index=worksheet_index - 1)

            # Fill cells
            ws_new.update_acell(TEMPLATE_C['description']['cell'],
                                TEMPLATE_C['description']['templ'].format(can_name, can_code, can_id, can_time, can_score))
            ws_new.update_acell(TEMPLATE_C['homepage']['cell'], TEMPLATE_C['homepage']['templ'].format(can_link))
            ws_new.update_acell(TEMPLATE_C['field']['cell'], TEMPLATE_C['field']['templ'].format(can_link))
            ws_new.update_acell(TEMPLATE_C['tee-times']['cell'], TEMPLATE_C['tee-times']['templ'].format(can_link))
            ws_new.update_acell(TEMPLATE_C['leaderboard']['cell'], TEMPLATE_C['leaderboard']['templ'].format(can_link))
            ws_new.update_acell(TEMPLATE_C['leaderboard_fr']['cell'], TEMPLATE_C['leaderboard_fr']['templ'].format(can_link))
            ws_new.update_acell(TEMPLATE_C['past-results']['cell'], TEMPLATE_C['past-results']['templ'].format(can_link))
            ws_new.update_acell(TEMPLATE_C['past-winners']['cell'], TEMPLATE_C['past-winners']['templ'].format(can_link))
            ws_new.update_acell(TEMPLATE_C['course']['cell'], TEMPLATE_C['course']['templ'].format(can_link))
            ws_new.update_acell(TEMPLATE_C['weather']['cell'], TEMPLATE_C['weather']['templ'].format(can_link))
    return "The template was successfully filled."


def main():
    """Main function"""
    sheet = create_spreadsheet()
    sheet_id = sheet.id
    filled = fill_spreadsheet(TOURS_LIST, sheet)
    delete_template_worksheets.main(sheet)
    return "{} Link to the spreadsheet: https://docs.google.com/spreadsheets/d/{}".format(filled, sheet_id)


if __name__ == "__main__":
    print(main())
