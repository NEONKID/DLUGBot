import requests, re

from bs4 import BeautifulSoup as bs
from base64 import b64decode as dec

LOCATION = {
    "죽전": {
        "교직원식당": "555",
        "학생식당": "556",
        "기숙사식당": "557"
    },

    "천안": {
        "교직원식당": "560",
        "학생식당": "561",
        "기숙사식당": "562"
    }
}


def requestFoodMenu(event):
    campus = event['location']['campus']
    restaurant = event['location']['restaurant']

    year = event['date']['year']
    weekofyear = event['date']['weekofyear']
    weekday = event['date']['weekday']

    LINK_HEAD = dec(b'aHR0cHM6Ly93d3cuZGFua29vay5hYy5rci93ZWIva29yLy0=').decode('utf-8')
    LINK_TAIL = dec(b'P3BfcF9pZD1Gb29kX1dBUl9mb29kcG9ydGxldCZwX3BfbGlmZWN5Y2xlPTAmcF9wX3N0YXRlPW5vcm1hbCZwX3BfbW9kZT12aWV3JnBfcF9jb2xfaWQ9Y29sdW1uLTImcF9wX2NvbF9wb3M9MiZwX3BfY29sX2NvdW50PTMmX0Zvb2RfV0FSX2Zvb2Rwb3J0bGV0X2FjdGlvbj12aWV3').decode('utf-8')
    SITE_LINK = LINK_HEAD + LOCATION[campus][restaurant] + LINK_TAIL

    # Form Data
    form_data = {
        "_Food_WAR_foodportlet_sYear": year,
        "_Food_WAR_foodportlet_sWeekOfYear": weekofyear
    }

    # HTTP POST Requests
    dku_req = requests.post(url=SITE_LINK, data=form_data)

    # HTML Source
    dku_html = dku_req.text

    # BeautifulSoup
    dku_soup = bs(dku_html, features='html5lib')

    # Menu Code
    # 1 = Mon, 2 = Tue, 3 = Wed, 4 = Thu, 5 = Fri, 6 = Sat
    dku_soup_request = dku_soup.find_all('tr')[weekday]

    # Menu Tables
    dku_soup_table = str(dku_soup_request.find_all('td')[1]).replace('<br/>', '\n').replace('&lt', '[').replace(
        '&gt', ']').replace('amp', '')

    # Final response
    dku_soup_remove_tag = re.sub('td', '', dku_soup_table, 0, re.I | re.S)
    dku_soup_response = re.sub('[/<>;\\\]', '', dku_soup_remove_tag, 0, re.I | re.S)

    result = {
        "success": "true"
    }

    if dku_soup_response == " ":
        result['message'] = "식단 메뉴가 존재하지 않습니다. \n(방학 중이거나 식당이 운영 중이지 않을 수 있습니다.)"
    else:
        result['message'] = dku_soup_response

    return result

