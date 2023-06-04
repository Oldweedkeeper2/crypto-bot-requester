# https://alfabit.org/api/v1/cashe/operations/Tether(USDT)%20TRC20
import asyncio
import json
from pprint import pprint
from typing import Dict, List
from bs4 import BeautifulSoup
import httpx
from playwright.async_api import async_playwright

from exchangers_manager.xml_parser import xml_parse
from manifests.exchangers_manifest import Exchangers
from manifests.tokens_manifest import Tokens
from exchangers_manager.normalizer import normalize

# https://expochange.org/xchange_TRX_to_SBERRUB/    xchange_COINFORM_to_COINTO
async def fetch_and_parse_data() -> List[Dict] or None:
    xml_data = httpx.get('https://expochange.org/tarifs/')
    # Create a BeautifulSoup object
    soup = BeautifulSoup(xml_data.text, 'html.parser')
    
    # Extract the desired information
    summary = soup.findAll('td', class_='tacursotd')
    coin_name = soup.findAll('div', class_='obmenlinetext')
    reserve = soup.findAll('td', class_='tarezervs')
    
    # Extract the text content from each element
    give_texts = [summary[div].text.replace('\xa0', ' ') for div in range(0, len(summary), 2)]
    get_texts = [summary[div].text.replace('\xa0', ' ') for div in range(1, len(summary), 2)]
    coin_from_name_texts = [(coin_name[div].text).strip(' ') for div in range(0, len(coin_name), 2)]
    coin_to_name_texts = [(coin_name[div].text).strip(' ') for div in range(1, len(coin_name), 2)]
    amount_texts = [div.text.strip() for div in reserve]
    grouped_data = []
    # formatter
    for index, values in enumerate(zip(give_texts, get_texts, coin_from_name_texts, coin_to_name_texts, amount_texts)):
        exchange_rate = '{:.8f}'.format(float(values[0].split(' ')[0]) / float(values[1].split(' ')[0]))
        
        bank = normalize(value=values[3])
        if bank == (None, None) or bank is None:
            break
        
        group_dict = {
            'exchange_rate': exchange_rate,
            'from_currency': values[2],
            'to_currency': bank,
            "min_exchange_amount": None,
            'reserve': values[4],
        }
        grouped_data.append(group_dict)
    return grouped_data


# pprint(asyncio.run(fetch_and_parse_data()))
