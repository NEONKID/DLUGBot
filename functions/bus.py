import requests
from base64 import b64decode as dec


# User agent
__USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
__CONTENT_TYPE = 'application/x-www-form-urlencoded; charset=UTF-8'
__headers = {'User-Agent': __USER_AGENT, 'Content-Type': __CONTENT_TYPE}


# Error / Info Message
__NONE_BUS = '해당 정류장에 도착할 버스 정보가 없습니다.'
__NOTICE_BUS = '상기 버스 정보는 1~2분 정도 차이가 있을 수 있으며 교통상황에 따라 달라질 수 있음을 참고하시기 바랍니다.'


# Cheonan Bus information
__CHEONAN_LINK = dec(b'aHR0cDovL2l0cy5jaGVvbmFuLmdvLmtyLw==').decode('utf-8')
__CHEONAN_PREDICT = dec(b'YmlzL3ByZWRpY3RJbmZvLmRv').decode('utf-8')
__CHEONAN_ROAD = dec(b'Y29tbW9uL2RyYXdBdHJkUm9hZC5kbw==').decode('utf-8')

__CHEONAN_BUS = '28500'

__CH_STATION = {
    "단국대학교": __CHEONAN_BUS + '1478',
    "단국대학교치대병원": __CHEONAN_BUS + '1595',
    "상명대학교": __CHEONAN_BUS + '0642'
}

__CH_ATDR = {
    "단국대학교": "만남로",
    "단국대학교치대병원": "망향로",
    "상명대학교": "망향로"
}


# SeongNam Bus information
__JUKJEON_LINK = dec(b'aHR0cDovL3d3dy5nYmlzLmdvLmtyL2diaXMyMDE0L3NjaEJ1c0FQSS5hY3Rpb24=').decode('utf-8')
__JUKJEON_BUS = '22800'
__JU_STATION = {
    "단국대정문": __JUKJEON_BUS + '1978',
    "죽전야외음악당": __JUKJEON_BUS + '0999',
    "단국대치과병원": __JUKJEON_BUS + '1736',
    "단국대인문관": __JUKJEON_BUS + '1981'
}


def getBusCheonan(station):
    """
    천안 캠퍼스 주변 버스 정류장 정보를 가져옵니다 \n
    (정보 제공: 천안버스정보 안내 시스템)

    :type station: string
    :param station: 정류장 이름
    :return:
        해당 정류장에 오는 버스 정보 \n
        천안의 경우, 버스 번호, 시간, 남은 정류장 표시
    """

    # Request & Response
    req = {'stopId': __CH_STATION[station.replace(' 정류장', '')]}
    res = requests.post(url=__CHEONAN_LINK + __CHEONAN_PREDICT, data=req, headers=__headers).json()

    # Final return messages
    result = ''
    info = ''

    # Get bus information message in Cheonan
    for bus in res:
        if bus['RTIME'] != 9999:
            info += '[' + str(bus['ROUTE_NAME']) + '번 (' + str(bus['ROUTE_EXPLAIN']) + ')]\n' + \
                    __convertTime(bus['RTIME']) + '후 도착 예정입니다.' + '\n' + '현재 위치: ' + \
                    str(bus['LAST_STOP_NAME']) + '\n' + '남은 버스 정류장: ' + str(bus['RSTOP']) + ' 정류장\n' + '차량 번호: ' + \
                    str(bus['PLATE_NO']) + '\n\n'

    if info == '':
        result += __NONE_BUS
    else:
        _atrReq = {
            "atrdNm": __CH_ATDR[station.replace(' 정류장', '')],
            "level": "9"
        }
        _atrHdr = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        _atrRes = requests.post(url=__CHEONAN_LINK + __CHEONAN_ROAD, headers=_atrHdr, data=_atrReq).json()
        for atdr in _atrRes:
            if 0 < atdr['SPED'] < 22:
                info += '※ ' + atdr['END_NM_NODE'] + "부터 " + atdr['STRT_NM_NODE'] + "까지 일부 정체.. \n"

        result += info + __NOTICE_BUS

    return result


def getBusJukjeon(station):
    """
        죽전 캠퍼스 주변 버스 정류장 정보를 가져옵니다 \n
        (정보 제공: 경기도 버스 안내 시스템)

        :type station: string
        :param station: 정류장 이름
        :return:
            해당 정류장에 오는 버스 정보 \n
            죽전의 경우, 버스 번호, 시간, 남은 정류장, 좌석 정보 (직행 버스 한정) 제공
    """

    # Bus crowded
    seatlist = {
        '0': '확인 불가',
        '1': '여유',
        '2': '보통',
        '3': '혼잡'
    }
    asc = '직행좌석형시내버스'

    # Request & Response
    req = {
        'cmd': 'searchBusStationJson',
        'stationId': __JU_STATION[station.replace(' 정류장', '')]
    }
    res = requests.post(url=__JUKJEON_LINK, data=req, headers=__headers).json()

    # Final return messages
    result = ''
    info = ''
    routetype = ''

    # Get bus information message
    for ai in res['result']['busArrivalInfo']:
        if ai['stationId'] == req['stationId']:
            if ai['plateNo1'] != '':
                for si in res['result']['busStationInfo']:
                    if ai['routeName'] == si['routeName']:
                        routetype = si['routeTypeName']
                        break

                seat = '좌석 현황: ' + ai['remainSeatCnt1'] + '자리 남음' if routetype == asc \
                    else '버스 인원: ' + seatlist[ai['crowded1']]

                info += '[' + str(ai['routeName']) + '번 (' + str(ai['routeDestName']) + ' 방면), ' + routetype + ']\n' \
                        + __convertTime(ai['predictTime1']) + '후 도착 예정입니다.' + '\n' \
                        + '현재 위치: ' + str(ai['stationNm1']) + '(' + str(ai['locationNo1']) + '번째 전)\n' \
                        + seat + '\n' + '차량 번호: ' + str(ai['plateNo1']) + '\n\n'

    if info == '':
        result += __NONE_BUS
    else:
        result += info + __NOTICE_BUS

    return result


def __convertTime(time):
    if int(time) >= 60:
        result = str(int(int(time) / 60)) + '시간 ' + str(int(time) % 60) + '분 ' if int(time) % 60 != 0 \
            else str(int(time) / 60) + '시간 '
    else:
        result = str(time) + '분 ' if int(time) != 0 else '잠시 '

    return result