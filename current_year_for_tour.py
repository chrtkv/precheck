#!/usr/bin/env python3

import requests

def main(tour_code):
    request_url = 'http://statdata.pgatour.com/r/current/schedule-v2.json'
    schedule_raw = requests.get(request_url)
    schedule_json = schedule_raw.json()
    current_years = schedule_json.get("currentYears")

    current_year_for_tour = current_years[tour_code.lower()]

    return current_year_for_tour
