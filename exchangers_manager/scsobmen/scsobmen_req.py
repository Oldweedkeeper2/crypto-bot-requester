import asyncio
from pprint import pprint
from typing import List, Dict

import httpx
from bs4 import BeautifulSoup

from exchangers_manager.normalizer import normalize
from manifests.exchangers_manifest import Exchangers
from manifests.tokens_manifest import Tokens


async def fetch_and_parse_data() -> List[Dict]:
    
    async with httpx.AsyncClient() as client:
        response = await client.get('https://scsobmen.com/tarifs/')
        response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the HTML elements that contain the data
    coin_names = soup.find_all('div', class_='tarif_curs_title_ins')
    coin_names = list(map(lambda x: x.text.replace('\n', ''), coin_names))
    give_get = soup.find_all('div', class_='tarif_curs_ins')
    give_get = list(map(lambda x: x.text.replace('\xa0', ' ').replace('\n', ''), give_get))
    reserve = soup.find_all('div', class_='tarif_curs_reserv_ins')
    reserve = list(map(lambda x: ''.join(x.text.split(' ')[1:3]), reserve))
    
    coin_from = [coin_names[x] for x in range(0, len(coin_names), 2)]
    coin_to = [coin_names[x] for x in range(1, len(coin_names), 2)]
    give = [give_get[x] for x in range(0, len(give_get), 2)]
    get = [give_get[x] for x in range(1, len(give_get), 2)]
    
    grouped_data = []
    for index, values in enumerate(zip(coin_from, coin_to, give, get, reserve)):
        exchange_rate = float(values[2].split(' ')[0]) / float(values[3].split(' ')[0])
        bank = normalize(value=values[1])
        if bank == (None, None) or bank is None:
            break
        group_dict = {
            'from_currency': values[0],
            'to_currency': bank,
            'exchange_rate': exchange_rate,
            "min_exchange_amount": None,
            'reserve': values[4]
        }
        grouped_data.append(group_dict)
    return grouped_data


# Run the function
# data = asyncio.run(fetch_and_parse_data())
# pprint(data)
