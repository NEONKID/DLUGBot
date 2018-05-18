import requests, re
from bs4 import BeautifulSoup

# Jukjeon information links
__JUKJEON_LINK = 'http://220.149.240.70/SeatWeb/domian5.asp'
__JUKJEON_VIEW_LINK = 'http://220.149.240.70/SeatWeb/roomview5.asp?room_no='

# Cheonan information links
__CHEONAN_LINK = 'http://203.237.217.8/EZ5500/SEAT/RoomStatus.aspx'

# Jukjeon Reading Room list
__JU_RR = {
    '1층 1열람실': 1,
    '1층 6열람실': 7,
    '2층 2열람실': 2,
    '2층 3열람실': 3,
    '2층 4열람실': 4,
    '2층 대학원열람실': 5,
    '법학 열람실': 8
}

# Cheonan Reading Room list
__CH_RR = {
    '지하1층 제1열람실 A구역': 1,
    '지하1층 제1열람실 B구역': 2,
    '지하1층 제1열람실 C구역': 3,
    '지하1층 제1열람실 D구역': 4,

    '1층 제2열람실 A구역': 5,
    '1층 제2열람실 B구역': 6,
    '1층 제2열람실 C구역': 7,
    '1층 제2열람실 D구역': 8,
    '1층 제2열람실 E구역': 9,
    '1층 제2열람실 F구역': 10,

    '1층 제3열람실 A구역': 11,
    '1층 제3열람실 B구역': 12,
    '1층 제3열람실 C구역': 13
}


def __requestRRInfoJukjeon(location):
    # HTML code for euc-kr(cp949) encoding
    res_html = requests.get(url=__JUKJEON_LINK).content
    res_soup = BeautifulSoup(res_html, features='html.parser')

    # currentTime
    res_soup_currentTime = res_soup.find_all('tr')[1]

    # Reading room number / view link
    rr_num = __JU_RR[location]
    rr_link = __JUKJEON_VIEW_LINK + str(rr_num)

    res_soup_location = res_soup.find_all('tr')[rr_num + 1] if rr_num > 5 else res_soup.find_all('tr')[rr_num + 2]

    # Total seats
    res_location_total = str(res_soup_location.find_all('td')[2].find_all('font', {'size': '-1'}))
    total_fin = re.findall('\d+', res_location_total)[1]

    # Using seats
    res_location_using = str(res_soup_location.find_all('td')[3].find_all('font', {'size': '-1'}))
    using_fin = re.findall('\d+', res_location_using)[1]
    using_comment = '총 ' + total_fin + '개 중 ' + using_fin + '개 사용'

    # Available seats
    res_location_avail = str(res_soup_location.find_all('td')[4].find_all('font', {'size': '-1'}))
    avail_fin = re.findall('\d+', res_location_avail)[1]

    # Utilization reading room
    res_location_util = str(res_soup_location.find_all('td')[5].find_all('font', {'size': '-1'}))
    util_fin = '열람실 사용률: ' + re.findall('\d+', res_location_util)[1] + '.' + re.findall('\d+', res_location_util)[
        2] + '%' \
        if len(re.findall('\d+', res_location_util)) == 3 \
        else '열람실 사용률: ' + re.findall('\d+', res_location_util)[1] + '%'

    if int(avail_fin) == 0:
        message = '현재 남아 있는 자리가 없습니다. \n\n' + '<자리 현황>\n' + using_comment + '\n' + util_fin
    else:
        message = '현재 ' + avail_fin + '자리가 남아있습니다. \n\n' + '<자리 현황>\n' + using_comment + '\n' + util_fin

    add_comment = '자세한 자리 현황을 보시려면 아래의 버튼을 클릭해주세요.'

    result = {
        'result': {
            'message': message + '\n\n' + add_comment,
            'link': rr_link
        },
        'success': 'true'
    }
    return result


def __requestRRInfoCheonan(location):
    # HTML code for utf8 encoding
    res_html = requests.post(url=__CHEONAN_LINK).text
    res_soup = BeautifulSoup(res_html, features='html.parser')

    # 이걸로 한방에 끝낼 수 있는 것을....
    # res_soup_list = res_soup.find_all('tr', {'onclick': "SelectRow(\'" + str(__CH_RR[location]) + "\')"})
    res_soup_list = res_soup.find_all('tr')[3]

    # 기준점으로 대체..
    idx = 4 * (__CH_RR[location] - 1)

    # Total seats
    res_location_total = str(res_soup_list('td')[__CH_RR[location] + idx])
    total_fin = re.findall('\d+', res_location_total)[3]

    # Using seats
    res_location_using = str(res_soup_list('td')[__CH_RR[location] + (idx + 1)])
    using_fin = re.findall('\d+', res_location_using)[3]
    using_comment = '총 ' + total_fin + '개 중 ' + using_fin + '개 사용'

    # Availalbe Seats
    res_location_avail = str(res_soup_list('td')[__CH_RR[location] + (idx + 2)])
    avail_fin = re.findall('\d+', res_location_avail)[3]

    # Utilization reading room
    res_location_util = str(res_soup_list('td')[__CH_RR[location] + (idx + 3)])
    util_fin = '열람실 사용률: ' + re.findall('\d+', res_location_util)[3] + '.' + re.findall('\d+', res_location_util)[
        4] + '%' \
        if len(re.findall('\d+', res_location_util)) == 5 \
        else '열람실 사용률: ' + re.findall('\d+', res_location_util)[3] + '%'

    if int(avail_fin) == 0:
        message = '현재 남아 있는 자리가 없습니다. \n\n' + '<자리 현황>\n' + using_comment + '\n' + util_fin
    else:
        message = '현재 ' + avail_fin + '자리가 남아있습니다. \n\n' + '<자리 현황>\n' + using_comment + '\n' + util_fin

    add_comment = '자세한 자리 현황을 보시려면 아래의 버튼을 클릭해주세요.'

    result = {
        'result': {
            'message': message + '\n\n' + add_comment,
            'link': __CHEONAN_LINK
        },
        'success': 'true'
    }
    return result


def requestRRInfo(event):
    if event['region'] == '죽전':
        _res = __requestRRInfoJukjeon(event['location'])

    elif event['region'] == '천안':
        _res = __requestRRInfoCheonan(event['location'])

    else:
        _res = {
            'error': 'Unknown region...',
            'success': 'false'
        }

    return _res