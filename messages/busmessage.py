import json
from functions import bus

keyboard = json.load(open('data/keyboard.json'))
busList = json.load(open('data/keyboard_Bus.json'))


def routeBus(request):
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