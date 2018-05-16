import json

keyboard = json.load(open('data/keyboard.json'))
busList = json.load(open('data/keyboard_Bus.json'))


# 요청한 메시지에 따라 응답 메시지 전송...
def getResMessage(topic):
    with open('data/resMsg.json') as msg_File:
        data = json.load(msg_File)

    if topic == '버스 언제 오지?':
        data[topic]['keyboard'] = busList

    else:
        data[topic]['keyboard'] = keyboard

    return data[topic]