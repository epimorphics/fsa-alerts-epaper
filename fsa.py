import requests
from enum import Enum

class AlertType(Enum):
    PRIN = 1
    AA = 2
    Alert = 3

def get_latest_alert():
    r = requests.get('https://data.food.gov.uk/food-alerts/id?&_view=full&_sort=-created&_limit=1')
    json = r.json()['items']
    if len(json) >= 1:
        return json[0]

def get_alert_type(alert):
    if ("http://data.food.gov.uk/food-alerts/def/PRIN" in alert["type"]):
        return AlertType.PRIN
    elif ("http://data.food.gov.uk/food-alerts/def/AA" in alert["type"]):
        return AlertType.AA
    else:
        return AlertType.Alert

