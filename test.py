import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import generate_tours_list
import precheck_date
from googleapiclient import discovery
from pprint import pprint

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", 
"https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('precheck-5c5daf9891d6.json', SCOPES)
gs = gspread.authorize(credentials)

sheet_name_template = "{} Testtttt-tournament checklist"
sheet_name = sheet_name_template.format(precheck_date.main())
template_id = '1RSARFhzrk4Cllu38qDrGihy9nbkBwpNmHq7wCxo9HPI'
t_list = generate_tours_list.main()

pga_tour_data_template = "PGA TOUR - {} ({}{}), Time = {},\nScore Type = {}"
korn_tour_data_template = "Korn Ferry - {} ({}{}), Time = {},\nScore Type = {}"

# Copy spreadsheet from template and share it
sheet = gs.copy(template_id, title=sheet_name, copy_permissions=True, )
sheet.share('kirill.chertkov@ix.co', perm_type='user', role='writer')

#sheet = gs.open(sheet_name)
spreadsheet_id = sheet.id

def get_actual_template_worksheet_index(tour_code):
    """Recieves tour code and returns actuall index for worksheet with template for appropriate tour"""
    list_of_worksheets = []
    list_of_indexes = {}
    service = discovery.build('sheets', 'v4', credentials=credentials)
    # The spreadsheet to request.
    #spreadsheet_id = spreadsheet_id
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


for element in t_list:
    if element["tour_code"] == 'R':
        pga_name = element['name']
        pga_code = element['tour_code']
        pga_id = element['tour_id']
        pga_score = element['score_type']
        pga_time = element['time_zone']
        pga_link = element['link']
        worksheet_index = get_actual_template_worksheet_index(pga_code)
        worksheet = sheet.get_worksheet(worksheet_index)
        worksheet_new = worksheet.duplicate(new_sheet_name=pga_name)
        worksheet_new.update_acell('B12', pga_tour_data_template.format(pga_name, pga_code, pga_id, pga_time, pga_score))

    if element["tour_code"] == 'H':
        korn_name = element['name']
        korn_code = element['tour_code']
        korn_id = element['tour_id']
        korn_score = element['score_type']
        korn_time = element['time_zone']
        korn_link = element['link']
        worksheet_index = get_actual_template_worksheet_index(korn_code)
        worksheet = sheet.get_worksheet(worksheet_index)
        worksheet_new = worksheet.duplicate(new_sheet_name=korn_name)
        worksheet_new.update_acell('B5', korn_tour_data_template.format(korn_name, korn_code, korn_id, korn_time, korn_score))



# worksheet.update_acell('C1', 'Lovejodz')
#print(worksheet_for_changes.get_all_values())

# for i in generate_tours_list.main():
#     print(i['name'])