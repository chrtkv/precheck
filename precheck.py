import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import generate_tours_list
import precheck_date
from googleapiclient import discovery
from pprint import pprint
import players_list
import current_year_for_tour
import delete_template_worksheets

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", 
"https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('precheck-5c5daf9891d6.json', SCOPES)
gs = gspread.authorize(credentials)

sheet_name_template = "{} Pre-tournament checklist"
sheet_name = sheet_name_template.format(precheck_date.main())
template_id = '1RSARFhzrk4Cllu38qDrGihy9nbkBwpNmHq7wCxo9HPI'
tours_list = generate_tours_list.main()

# load templates
with open('templates/tournaments.json') as template_data:
    template = json.load(template_data)
template_r = template['r']
template_h = template['h']
template_c = template['c']
template_m = template['m']
template_s = template['s']

# Copy spreadsheet from template and share it
sheet = gs.copy(template_id, title=sheet_name, copy_permissions=True)
sheet.share('kirill.chertkov@ix.co', perm_type='user', role='writer')
spreadsheet_id = sheet.id

#sheet = gs.open(sheet_name)

def get_actual_template_worksheet_index(tour_code):
    """Recieves tour code and returns actuall index for worksheet with template for appropriate tour"""
    list_of_worksheets = []
    list_of_indexes = {}
    service = discovery.build('sheets', 'v4', credentials=credentials)
    # The ranges to retrieve from the spreadsheet.
    ranges = []  # TODO: Update placeholder value.
    # True if grid data should be returned.
    # This parameter is ignored if a field mask was set in the request.
    include_grid_data = False  # TODO: Update placeholder value.
    request = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
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


for element in tours_list:
    if element["tour_code"] == 'R':
        pga_name = element['name']
        pga_code = element['tour_code']
        pga_id = element['tour_id']
        pga_score = element['score_type']
        pga_time = element['time_zone']
        pga_link = element['link']
        pga_year = current_year_for_tour.main(pga_code)
        pga_players = players_list.main(pga_code.lower(), pga_id)
        worksheet_index = get_actual_template_worksheet_index(pga_code)
        worksheet = sheet.get_worksheet(worksheet_index)
        ws_new = worksheet.duplicate(new_sheet_name=pga_name, insert_sheet_index=1)

        # Fill cells
        ws_new.update_acell(template_r['description']['cell'], 
        template_r['description']['templ'].format(pga_name, pga_code, pga_id, pga_time, pga_score))
        ws_new.update_acell(template_r['homepage']['cell'], template_r['homepage']['templ'].format(pga_link))
        ws_new.update_acell(template_r['field']['cell'], template_r['field']['templ'].format(pga_link))
        ws_new.update_acell(template_r['tee-times']['cell'], template_r['tee-times']['templ'].format(pga_link))
        ws_new.update_acell(template_r['leaderboard']['cell'], template_r['leaderboard']['templ'].format(pga_year, pga_link))
        ws_new.update_acell(template_r['yahoo']['cell'], template_r['yahoo']['templ'].format(pga_year, pga_id))
        ws_new.update_acell(template_r['korean']['cell'], template_r['korean']['templ'].format(pga_year, pga_link))
        ws_new.update_acell(template_r['past-results']['cell'], template_r['past-results']['templ'].format(pga_link))
        ws_new.update_acell(template_r['past-winners']['cell'], template_r['past-winners']['templ'].format(pga_link))
        ws_new.update_acell(template_r['course']['cell'], template_r['course']['templ'].format(pga_link))
        ws_new.update_acell(template_r['weather']['cell'], template_r['weather']['templ'].format(pga_link))
        ws_new.update_acell(template_r['pinsheet']['cell'], template_r['pinsheet']['templ'].format(pga_year, pga_link))

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
        ch_year = current_year_for_tour.main(ch_code)
        ch_players = players_list.main(ch_code.lower(), ch_id)
        worksheet_index = get_actual_template_worksheet_index(ch_code)
        worksheet = sheet.get_worksheet(worksheet_index)
        ws_new = worksheet.duplicate(new_sheet_name=ch_name, insert_sheet_index=worksheet_index - 1)

        # Fill cells
        ws_new.update_acell(template_s['description']['cell'], 
        template_s['description']['templ'].format(ch_name, ch_code, ch_id, ch_time, ch_score))
        ws_new.update_acell(template_s['homepage']['cell'], template_s['homepage']['templ'].format(ch_link))
        ws_new.update_acell(template_s['field']['cell'], template_s['field']['templ'].format(ch_link))
        ws_new.update_acell(template_s['tee-times']['cell'], template_s['tee-times']['templ'].format(ch_link))
        ws_new.update_acell(template_s['leaderboard']['cell'], template_s['leaderboard']['templ'].format(ch_year, ch_link))
        ws_new.update_acell(template_s['past-results']['cell'], template_s['past-results']['templ'].format(ch_link))
        ws_new.update_acell(template_s['past-winners']['cell'], template_s['past-winners']['templ'].format(ch_link))
        ws_new.update_acell(template_s['course']['cell'], template_s['course']['templ'].format(ch_link))
        ws_new.update_acell(template_s['weather']['cell'], template_s['weather']['templ'].format(ch_link))

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
        worksheet_index = get_actual_template_worksheet_index(korn_code)
        worksheet = sheet.get_worksheet(worksheet_index)
        ws_new = worksheet.duplicate(new_sheet_name=korn_name, insert_sheet_index=worksheet_index - 1)

        # Feel cells
        ws_new.update_acell(template_h['description']['cell'],
        template_h['description']['templ'].format(korn_name, korn_code, korn_id, korn_time, korn_score))
        ws_new.update_acell(template_h['homepage']['cell'], template_h['homepage']['templ'].format(korn_link))
        ws_new.update_acell(template_h['field']['cell'], template_h['field']['templ'].format(korn_link))
        ws_new.update_acell(template_h['tee-times']['cell'], template_h['tee-times']['templ'].format(korn_link))
        ws_new.update_acell(template_h['leaderboard']['cell'], template_h['leaderboard']['templ'].format(korn_link))
        ws_new.update_acell(template_h['past-results']['cell'], template_h['past-results']['templ'].format(korn_link))
        ws_new.update_acell(template_h['past-winners']['cell'], template_h['past-winners']['templ'].format(korn_link))
        ws_new.update_acell(template_h['course']['cell'], template_h['course']['templ'].format(korn_link))
        ws_new.update_acell(template_h['weather']['cell'], template_h['weather']['templ'].format(korn_link))

    if element["tour_code"] == 'C':
        can_name = element['name']
        can_code = element['tour_code']
        can_id = element['tour_id']
        can_score = element['score_type']
        can_time = element['time_zone']
        can_link = element['link']
        worksheet_index = get_actual_template_worksheet_index(can_code)
        worksheet = sheet.get_worksheet(worksheet_index)
        ws_new = worksheet.duplicate(new_sheet_name=can_name, insert_sheet_index=worksheet_index - 1)

        # Feel cells
        ws_new.update_acell(template_c['description']['cell'],
        template_c['description']['templ'].format(can_name, can_code, can_id, can_time, can_score))
        ws_new.update_acell(template_c['homepage']['cell'], template_c['homepage']['templ'].format(can_link))
        ws_new.update_acell(template_c['field']['cell'], template_c['field']['templ'].format(can_link))
        ws_new.update_acell(template_c['tee-times']['cell'], template_c['tee-times']['templ'].format(can_link))
        ws_new.update_acell(template_c['leaderboard']['cell'], template_c['leaderboard']['templ'].format(can_link))
        ws_new.update_acell(template_c['leaderboard_fr']['cell'], template_c['leaderboard_fr']['templ'].format(can_link))
        ws_new.update_acell(template_c['past-results']['cell'], template_c['past-results']['templ'].format(can_link))
        ws_new.update_acell(template_c['past-winners']['cell'], template_c['past-winners']['templ'].format(can_link))
        ws_new.update_acell(template_c['course']['cell'], template_c['course']['templ'].format(can_link))
        ws_new.update_acell(template_c['weather']['cell'], template_c['weather']['templ'].format(can_link))

delete_template_worksheets.main(sheet)