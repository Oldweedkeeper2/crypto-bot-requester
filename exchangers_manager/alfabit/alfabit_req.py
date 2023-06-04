# https://alfabit.org/api/v1/cashe/operations/Tether(USDT)%20TRC20
import asyncio
import json
from pprint import pprint
from typing import Dict, List, Coroutine

import httpx

from exchangers_manager.normalizer import normalize
from exchangers_manager.xml_parser import xml_parse
from manifests.tokens_manifest import Tokens


async def gather_with_concurrency() -> List[Dict]:
    tasks = [httpx.get(f'https://alfabit.org/api/v1/cashe/operations/{token}') for token in Tokens.tokens_init_alfabit
             if token.replace(')', '').split('(')[-1] in Tokens.tokens_ABB]
    
    fetched_data = await asyncio.gather(*tasks)
    combined_data = [item for sublist in fetched_data for item in sublist]
    return combined_data


# fast, multiply token search method
async def fetch_and_parse_data() -> List[Dict]:
    parsed_combined_data = []
    
    async def fetch_data(token):
        nonlocal parsed_combined_data
        async with httpx.AsyncClient() as client:
            response = await client.get(
                    f'https://alfabit.org/api/v1/cashe/operations/{token}')
            return json.loads(response.text)
    
    async def combine_data():
        tasks = [fetch_data(token) for token in Tokens.tokens_init_alfabit if
                 token.replace(')', '').split('(')[-1] in Tokens.tokens_ABB]
        fetched_data = await asyncio.gather(*tasks)
        for item in range(len(fetched_data)):
            for subitem in fetched_data[item]:
                bank = normalize(
                        value=subitem['buy_currency']['code'].replace("(", " ").replace(")", "").replace('cashin',
                                                                                                         'Cashin'))
                if bank == (None, None) or bank is None:
                    break
                alfabit_data = {
                    "from_currency": Tokens.tokens_ABB[item],
                    "to_currency": bank,
                    "exchange_rate": subitem['exchange_rate'],
                    "min_exchange_amount": subitem['min_buy'],
                    "reserve": subitem["reserv_value"]
                }
                parsed_combined_data.append(alfabit_data)
        
        return parsed_combined_data
    
    combined_data = await combine_data()
    
    return combined_data


# low, single token search method
async def check_exchange_rate(coin_from: str, coin_to: str) -> List[Dict]:
    xml_data = httpx.get(f'https://alfabit.org/api/v1/cashe/operations/detail/{coin_from}/{coin_to}')
    xml_data = json.loads(xml_data.text)
    
    return xml_data


pprint(asyncio.run(check_exchange_rate('Сбербанк(RUB)', 'Ethereum(ETH)')))
# for token in Tokens.tokens_init_alfabit:
#     print(token)
#     print(token.replace(')', '').split('(')[-1])
#     print(token.replace(')', '').split('(')[-1] in Tokens.tokens_ABB)
# print([token for token in Tokens.tokens_init_alfabit
#        if token.replace(')', '').split('(')[1] in Tokens.tokens_ABB])
# pprint(asyncio.run(fetch_and_parse_data()))
