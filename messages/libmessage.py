import json
from .loadresmsg import rrCheonan, rrJukjeon
from functions import dkurr


# 요청한 도서관의 좌석 현황을 가져옵니다..
def getRRSeat(topic):
    """
    카카오톡에서 사용자가 입력한 열람실 정보를 받는 함수

    :type topic: string
    :param topic: 열람실 이름
    :return: 카카오톡에 링크 메시지로 반환

    """

    data = None
    if topic[1:3] == '죽전':
        with open('data/rrMenu_Jukjeon.json') as msg_File:
            data = json.load(msg_File)

    elif topic[1:3] == '천안':
        with open('data/rrMenu_Cheonan.json') as msg_File:
            data = json.load(msg_File)

    elif topic == '죽전열람실':
        with open('data/rrMenu.json') as msg_File:
            data = json.load(msg_File)
        data[topic]['keyboard'] = rrJukjeon
        return data[topic]

    elif topic == '천안열람실':
        with open('data/rrMenu.json') as msg_File:
            data = json.load(msg_File)
        data[topic]['keyboard'] = rrCheonan
        return data[topic]

    _request = {
        'region': topic[1:3],
        'location': topic[4:]
    }
    response = dkurr.requestRRInfo(_request)

    if response['success'] != 'true':
        data[topic]['message']['text'] = topic + '\n\n' + '잘못된 요청입니다.'
    else:
        data[topic]['message']['text'] = topic + '\n\n' + response['result']['message']
        data[topic]['message']['message_button']['label'] = '좌석 배치도 보기'
        data[topic]['message']['message_button']['url'] = response['result']['link']

    data[topic]['keyboard'] = rrJukjeon if topic[1:3] == '죽전' else rrCheonan
    return data[topic]