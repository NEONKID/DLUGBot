import json, datetime

from functions import dkufood
from .loadresmsg import restList, keyboard


# 요청한 식당의 식단 메뉴를 가져옵니다..
def getRestMenu(topic):
    with open('data/restMenu.json') as msg_File:
        data = json.load(msg_File)

    if topic == "처음으로..":
        data[topic]['keyboard'] = keyboard
        return data[topic]

    now = datetime.datetime.now()

    _request = {
        "location": {
            "campus": topic[1:3],
            "restaurant": topic[4:]
        },

        "date": {
            "year": now.year,
            "weekofyear": now.isocalendar()[1],
            "weekday": now.weekday() + 1
        }
    }

    result = dkufood.requestFoodMenu(_request)

    data[topic]['message']['text'] = topic + "\n\n" + result['message']
    data[topic]['keyboard'] = restList

    return data[topic]