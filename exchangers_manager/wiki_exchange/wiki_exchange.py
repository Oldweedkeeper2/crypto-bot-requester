import asyncio
import json
from pprint import pprint
from typing import Dict

import httpx
from bs4 import BeautifulSoup

from manifests.exchangers_manifest import Exchangers
from manifests.tokens_manifest import Tokens


# забанен на ip


async def fetch_and_parse_id(file) -> Dict:
    extracted_data = {}
    with open(file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    coin_ids = soup.find_all('button', class_='val-btn')
    
    for coin_id in coin_ids:
        # Extract the 'psid' attribute from the button
        psid = coin_id['psid']
        title = coin_id.find('div', class_='val-title').text
        
        # Append the extracted data to the list as a dictionary
        extracted_data[title] = psid
    return extracted_data


async def check_direction(data, coin_from: str, coin_to: str):
    coin_from_id = data[coin_from]
    coin_to_id = data[coin_to]
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'https://wiki-exchange.com/check_direction?psid1={coin_from_id}&psid2={coin_to_id}&direct=false')
        response.raise_for_status()
    response = json.loads(response.text)
    response = response['value']
    exchange_rate = "{:.8f}".format(float(response['out']) / float(response['in']))
    group_dict = {
        'from_currency': response['in_valute'],
        'to_currency': response['out_valute'],
        'exchange_rate': exchange_rate,
        'minamount': response['in_min'],
        "reserve": response['reserve']
    }
    return group_dict


# for index, values in enumerate(zip(coin_from, coin_to, give, get)):
#     if values[0] in Tokens.tokens_ABB:  # Append only needed exchangers
#         group_dict = {
#             'from:': values[0],
#             'to:': values[1],
#             'give:': values[2],
#             'get:': values[3]
#         }
#         grouped_data.append(group_dict)
#
# return grouped_data


# Run the function
data_in = asyncio.run(fetch_and_parse_id('temp.html'))
data_out = asyncio.run(fetch_and_parse_id('temp_out.html'))
data_dir = asyncio.run(check_direction(data=data_in, coin_from='USDT ERC20', coin_to='Solana'))

# pprint(data_in)
# pprint(data_out)
pprint(data_dir)
