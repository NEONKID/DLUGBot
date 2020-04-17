import json

from functions import dkufood
from .loadresmsg import restList, keyboard


# 요청한 식당의 식단 메뉴를 가져옵니다..
def getRestMenu(topic):
    """
    카카오톡에서 사용자의 요청을 받아 원하는 식당 정보를 받고,
    메시지로 반환하는 함수

    :type topic: string
    :param topic: 메뉴 이름
    :return: 카카오톡에 일반 메시지로 반환
    """

    with open('data/restMenu.json') as msg_File:
        data = json.load(msg_File)

    if topic == "처음으로..":
        data[topic]['keyboard'] = keyboard
        return data[topic]

    _request = {
        "location": {
            "campus": topic[1:3],
            "restaurant": topic[4:]
        }
    }

    result = dkufood.requestFoodMenu(_request)

    data[topic]['message']['text'] = topic + "\n\n" + result['message']
    data[topic]['keyboard'] = restList

    return data[topic]