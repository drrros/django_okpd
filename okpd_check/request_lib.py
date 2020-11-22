import requests
from django.db import IntegrityError
from bs4 import BeautifulSoup
import time
import re
from okpd_check.models import Record
from concurrent.futures import ThreadPoolExecutor
import random
import datetime


def check_inner(code):
    zakupki_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }
    garant_headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Authorization": "Basic Z2FyYW50QGFrYml6LnJ1OjJUalhFNWJq",
        "Cookie": "JSESSIONID=nhzf83k7uune3ngbuvxke16p",
        "Referer": "http://okpd.garant.ru/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    zakupki_req_addr = f'https://zakupki.gov.ru/epz/ktru/search/results.html?searchString={code}&morphology=on'
    garant_req_addr = f'http://api/{code}&OkpdSearch[name]=&OkpdSearch[podbor]='
    ret_dict = {}
    query = Record.objects.filter(okpd=code).first()
    if query and query.date_changed.replace(tzinfo=None) > datetime.datetime.utcnow() - datetime.timedelta(hours=2):
        ret_dict[code] = {
            'ktru_records_count': query.ktru_records_count,
            'isCanceled':query.isCanceled,
            'zapret':query.zapret,
            'ogranichenia':query.ogranichenia,
            'preimuschestvo':query.preimuschestvo,
            'dopusk':query.dopusk,
            'perechen':query.perechen,
            'forma':query.forma,
            'tk':query.tk,
            'efektivnost':query.efektivnost,
            'perechenTryUIS':query.perechenTryUIS,
            'nepubl':query.nepubl
        }
        return ret_dict
    else:
        got_result = False
        while not got_result:
            time.sleep(random.randint(0, 3))
            time_delay = datetime.datetime.utcnow()
            content_zak = requests.get(zakupki_req_addr, headers=zakupki_headers)
            content_gar = requests.get(garant_req_addr, headers=garant_headers)
            if time_delay < datetime.datetime.utcnow() - datetime.timedelta(seconds=30):
                return {'timeout': True}
            if content_zak.status_code == requests.codes.ok and content_gar.status_code == requests.codes.ok:
                got_result = True
                try:
                    garant_resp_dict = content_gar.json()['models'][0].copy()
                except IndexError:
                    ret_dict[code] = {
                        'ktru_records_count': 'Код не найден',
                        'isCanceled': False,
                        'zapret': '0',
                        'ogranichenia': '0',
                        'preimuschestvo': '0',
                        'dopusk': '0',
                        'perechen': '0',
                        'forma': '0',
                        'tk': '0',
                        'efektivnost': '0',
                        'perechenTryUIS': '0',
                        'nepubl': '0',
                    }
                    return ret_dict

                # Zakupki
                soup = BeautifulSoup(content_zak.text, "html5lib")
                element = soup.find("div", class_="search-results__total")

                #Garant

                if query:
                    query.date_changed = datetime.datetime.utcnow()
                    query.save()
                else:
                    rec = Record(okpd=code,
                                 ktru_records_count=element.text.strip(),
                                 isCanceled=any([garant_resp_dict['isCanceled'], 'Исключен' in garant_resp_dict['name']]),
                                 zapret=garant_resp_dict['zapret'],
                                 ogranichenia=garant_resp_dict['ogranichenia'],
                                 preimuschestvo=garant_resp_dict['preimuschestvo'],
                                 dopusk=garant_resp_dict['dopusk'],
                                 perechen=garant_resp_dict['perechen'],
                                 forma=garant_resp_dict['forma'],
                                 tk=garant_resp_dict['tk'],
                                 efektivnost=garant_resp_dict['efektivnost'],
                                 perechenTryUIS=garant_resp_dict['perechenTry'],
                                 nepubl=garant_resp_dict['nePazmeschaetncya']
                                 )
                    try:
                        rec.save()
                    except IntegrityError:
                        pass
                if element:
                    ret_dict[code] = {
                        'ktru_records_count': element.text.strip(),
                        'isCanceled':any([garant_resp_dict['isCanceled'], 'Исключен' in garant_resp_dict['name']]),
                        'zapret':garant_resp_dict['zapret'],
                        'ogranichenia':garant_resp_dict['ogranichenia'],
                        'preimuschestvo':garant_resp_dict['preimuschestvo'],
                        'dopusk':garant_resp_dict['dopusk'],
                        'perechen':garant_resp_dict['perechen'],
                        'forma':garant_resp_dict['forma'],
                        'tk':garant_resp_dict['tk'],
                        'efektivnost':garant_resp_dict['efektivnost'],
                        'perechenTryUIS':garant_resp_dict['perechenTry'],
                        'nepubl':garant_resp_dict['nePazmeschaetncya']
                    }
                    return ret_dict


def check_codes(code_list:str, check_groups):
    if check_groups:
        regexp = re.compile(r'\d\d\.\d\d\.\d\d')
    else:
        regexp = re.compile(r'\d\d\.\d\d\.\d\d\.\d\d\d')
    match = re.findall(regexp, code_list)
    code_list = list(set(match))
    with ThreadPoolExecutor(max_workers=10) as executor:
        ret_list = executor.map(check_inner, code_list)
    return list(ret_list)

if __name__ == '__main__':
    pass
