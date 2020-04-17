from .loadresmsg import *


# 요청한 메시지에 따라 응답 메시지 전송...
def getResMessage(topic):
    """
    카카오톡에서 사용자가 입력한 메인 메뉴를 받는 함수

    :type topic: string
    :param topic: 메인 메시지
    :return: 각 메시지에 정해진 메시지로 반환

    """

    with open('data/resMsg.json') as msg_File:
        data = json.load(msg_File)

    if topic == '오늘의 식단 메뉴는?':
        data[topic]['keyboard'] = restList

    elif topic == '버스 언제 오지?':
        data[topic]['keyboard'] = busList

    elif topic == '열람실 자리 확인':
        data[topic]['keyboard'] = rrCampus

    else:
        data[topic]['keyboard'] = keyboard

    return data[topic]