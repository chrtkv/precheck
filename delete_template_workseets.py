#!/usr/bin/env python3

import gspread
import re

def main(spreadsheet):
    list_of_templates = ['PGA TOUR', 'Champions', 'Korn Ferry', 'Mackenzie-Canada', 'Latinoamerica', 'China']
    worksheets_list = spreadsheet.worksheets()

    for i in worksheets_list:
        worksheet_name = re.split('\'', str(i))[1]
        if worksheet_name in list_of_templates:
            spreadsheet.del_worksheet(i)