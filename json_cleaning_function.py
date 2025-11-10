from enum import Enum

class Meal(Enum):
    """Docstring for Meal."""
    TC_BREAK_FAST = "breakfast"
    TC_LUNCH_NORMAL = "lunchNormal"
    TC_LUNCH_SPECIAL = "lunchSpecial"

def find_by_date(date, json):
    for data in json:
        if data["date"] == date:
            return data
        else:
            return "Error: No data matched with date"
 