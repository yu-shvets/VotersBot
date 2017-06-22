from urllib import request
import xml.etree.cElementTree as ET


URL_1 = 'https://www.drv.gov.ua/apex/RDM$ADR.pgetATO?p_F7571=0'
URL_2 = 'https://www.drv.gov.ua/apex/RDM$ADR.pgetGEON?p_F7571='
URL_3 = 'https://www.drv.gov.ua/apex/RDM$ADR.pgetBUILDS?p_F3301='
URL_4 = 'https://www.drv.gov.ua/apex/RDM$ADR.p_getAreaBld?p_F3311='
API_KEY = 'YUFKSXF1ZmJlRHA0TG9SUVRKVnFsSkxiN2ZTaC9LeC9UOVMwWTIrTzExUT0='

districts = (
    'Голосіївський',
    'Дарницький',
    'Деснянський',
    'Дніпровський',
    'Оболонський',
    'Печерський',
    'Подільський',
    'Святошинський',
    'Солом’янський',
    'Шевченківський',
)


def api_request(url):

    file = request.urlopen(url)

    tree = ET.parse(file)
    root = tree.getroot()

    return root


def get_street_number(district, street):

    root = api_request(url=URL_1 + '41607' + '&pKey=' + API_KEY)

    district_number = ''

    try:
        for i in range(len(root)):
            if district in root[i][5].text:
                district_number = root[i][3].text
    except IndexError:
        return False

    root = api_request(url=URL_2 + district_number + '&pKey=' + API_KEY)

    street_number = ''

    try:
        for i in range(len(root)):
            if root[i][4].text == street:
                street_number = root[i][1].text
    except IndexError:
        return False

    return street_number


def get_building_list(district, street):

    buildings_list = []

    street_number = get_street_number(district, street)

    root = api_request(url=URL_3 + street_number + '&pKey=' + API_KEY)

    try:

        for i in range(len(root)):
            buildings_list.append(root[i][2].text)
    except IndexError:
        return False

    return street_number, buildings_list


def show_address(street_number, building):

    root = api_request(url=URL_3 + street_number + '&pKey=' + API_KEY)

    building_number = ''

    try:
        for i in range(len(root)):
            if root[i][2].text == building:
                building_number = root[i][1].text
    except IndexError:
        return 'Помилкові дані.'

    root = api_request(url=URL_4 + building_number + '&pKey=' + API_KEY)

    try:
        address = root[0][4].text + ', ' + root[0][5].text
    except IndexError:
        return 'Помилкові дані.'

    return address
