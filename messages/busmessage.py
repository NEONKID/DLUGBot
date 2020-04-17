import json

from functions import bus
from .loadresmsg import busList, keyboard


def routeBus(request):
    """
    카카오톡에서 요청 받은 버스 정보를 가지고, 메시지로 반환하는 함수

    :type request: JSON
    :param request: ``{ location: 지역 이름 (캠퍼스), station: 정류장 이름 }``
    :return: 요청 성공 여부와 메시지를 JSON 형태로 전달
    ``{ result: { success: 요청 여부, message: 실시간 버스 정보 메시지 } }``

    """

    try:
        if request['location'] == '죽전':
            _res = {
                'message': bus.getBusJukjeon(request['station']),
                'success': 'true'
            }
        elif request['location'] == '천안':
            _res = {
                'message': bus.getBusCheonan(request['station']),
                'success': 'true'
            }
        else:
            _res = {
                'error': 'Unknown Location...',
                'success': 'false'
            }
        return _res

    except KeyError:
        _res = {
            'error': 'Unknown station...',
            'success': 'false'
        }
        return _res


def getBusInfo(topic):
    """
    카카오톡에서 사용자가 입력한 정류장 이름을 받는 함수

    :type topic: string
    :param topic: 정류장 이름
    :return: 카카오톡에 실제 보여지는 메시지로 반환

    """

    with open('data/busMenu.json') as msg_File:
        data = json.load(msg_File)

    if topic == "처음으로..":
        data[topic]['keyboard'] = keyboard
        return data[topic]

    _request = {
        'location': topic[1:3],
        'station': topic[4:]
    }
    result = routeBus(_request)

    if result['success'] != 'true':
        data[topic]['message']['text'] = topic + '\n\n' + '잘못된 요청입니다.'
    else:
        data[topic]['message']['text'] = topic + '\n\n' + result['message']

    data[topic]['keyboard'] = busList
    return data[topic]