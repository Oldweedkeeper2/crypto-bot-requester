# wait ~10sec
import asyncio
from pprint import pprint
from typing import List, Dict

import httpx
from bs4 import BeautifulSoup

from manifests.tokens_manifest import Tokens


# only couple, not all views

async def fetch_id() -> List:
    async with httpx.AsyncClient() as client:
        response = await client.get('https://royal.cash/lite/f1/buy/all/')
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the HTML elements that contain the data
    # This is just a placeholder, you'll need to replace it with the actual criteria
    data_elements = soup.find_all('a')
    data_elements = data_elements[28:-16]
    data_elements = list(map(lambda x: x.get('href')[:-1], data_elements))
    data_elements = list(filter(lambda x: x in Tokens.tokens_ABR_lower, data_elements))
    
    return data_elements


async def track_a_couple(coin_from: str, coin_to: str) -> Dict:
    parsed_data = {}
    if coin_from != coin_to:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://royal.cash/lite/f1/buy/all/{coin_from}/all/{coin_to}/')
        
        soup = BeautifulSoup(response.text, 'html.parser')
        data_elements = soup.find_all('p')
        try:
            data_elements.pop(1)
        except:
            return parsed_data
        data_elements = list(
                map(lambda x: x.text.replace('  ', '').replace('\r\n', '').split(':')[1], data_elements[:-1]))
        give_get = data_elements[1].replace(' — ', ' ').split(' ')
        exchange_rate = '{:.8f}'.format(float(give_get[0]) / float(give_get[2]))
        parsed_data = {
            'from_currency:': give_get[1],
            'to_currency:': give_get[3],
            'exchange_rate': exchange_rate,
            'minamount': data_elements[0].split(' ')[0]
        }
    return parsed_data


# # Run the example function
l = ['busd', 'doge', 'bnb', 'atom', 'link', 'bat', 'avax']

# data = asyncio.run(track_a_couple('usdc-trc20', 'bitcoin'))
# pprint(data)
