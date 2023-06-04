import asyncio
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from manifests.exchangers_manifest import Exchangers


async def parse_exchange_rates(from_currency, to_currency):
    rs = requests.get(f'https://www.bestchange.ru/{from_currency}-to-{to_currency}.html')
    root = BeautifulSoup(rs.content, 'html.parser')
    data = []
    for tr in root.select('#content_table > tbody > tr'):
        exchanger_name = tr.select_one('td.bj .pc .ca').get_text(strip=True)
        
        [give_el, get_el] = tr.select('td.bi')
        give = give_el.select_one('.fs').get_text(strip=False).split(' ')
        get = get_el.get_text(strip=False).split(' ')
        exchange_rate = give[0]
        in_currency = ''.join(give[1:])
        out_currency = ''.join(get[1:])
        if exchanger_name in Exchangers.exchangers_valid_name:
            data.append(
                    {'exchanger_name': exchanger_name,
                     'exchange_rate': exchange_rate,
                     'in_currency': in_currency,
                     'out_currency': out_currency
                     }
            )
            
    data = sorted(data, key=lambda x: float(x['exchange_rate']))
    
    return data


pprint(asyncio.run(parse_exchange_rates('usd-coin', 'avalanche')))

