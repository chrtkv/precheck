"""Returns date of pre-check call (Wednesday)
    Format: mm.dd.yy"""
import re
import calendar

from bs4 import BeautifulSoup

import get_mail

def get_precheck_date(email_text):
    """Returns date of pre-check call (Wednesday)
    Format: mm.dd.yy"""
    # format text
    body_readable = BeautifulSoup(email_text, features='html5lib')
    # convert to string
    body_string = str(body_readable)
    # convert text to list.
    list_for_parsing = re.split(r"\n", body_string)

    for element in list_for_parsing:
        if "week of" in element.lower():
            week = element

    list_for_parsing = re.split(r" +", week)

    for element in list_for_parsing:
        if element in calendar.month_name:
            month_string = element
            month = list(calendar.month_name).index(element)
        if re.compile("^20[1,2][0-9]").match(element):
            year = int(element[2:])

    day = int(list_for_parsing[list_for_parsing.index(month_string) + 1]) + 2

    precheck_date = "{:02d}.{:02d}.{:02d}".format(month, day, year)

    return precheck_date

def main():
    """Main function"""
    return get_precheck_date(get_mail.main())