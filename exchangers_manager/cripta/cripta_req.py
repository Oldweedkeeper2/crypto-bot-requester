# https://alfabit.org/api/v1/cashe/operations/Tether(USDT)%20TRC20
import asyncio
import json
import re
from pprint import pprint
from typing import Dict, List

import httpx
from bs4 import BeautifulSoup

from exchangers_manager.xml_parser import xml_parse
from manifests.tokens_manifest import Tokens

# coming soon
# сайт отвалился) https://cripta.cc/specific_ways
# https://cripta.cc/pair/59/101 это вилка
# https://cripta.cc/ways/59 это поиск вилки


data1 = {'direction_from': 161,
         'direction_to': 44,
         'is_from': False}
r = httpx.get('https://cripta.cc')


async def fetch_and_parse_data():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://cripta.cc/')
        response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the <script> tag that contains the 'api' variable
    script_tag = soup.find('script', text=re.compile('var api ='))
    
    # Extract the JSON string from the script tag
    json_str = re.search('var api = ({.*?});', script_tag.string).group(1)
    
    # Parse the JSON string into a Python dictionary
    api_data = json.loads(json_str)
    return api_data


async def accept_ways_by_direction(token_id: int) -> List:
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://cripta.cc/ways/{token_id}')
        response.raise_for_status()
    return json.loads(response.text)


async def name_by_id(data: List[Dict]) -> List[Dict]:
    # Initialize an empty list to store the extracted data
    extracted_data = []
    
    # Iterate over the data
    for item in data:
        # Extract the 'id', 'currency', 'name_ru', and 'name_en' values
        id_value = item['id']
        currency = item['currency']
        name_ru = item['name_ru']
        
        # Append the extracted data to the list as a dictionary
        extracted_data.append({
            'id': id_value,
            'currency': currency,
            'name_ru': name_ru,
        })
    
    return extracted_data


async def dict_by_id(data: List[Dict], token_id: list) -> Dict:
    # Iterate over the data
    for item in data:
        if item['id'] == token_id:
            return item

    


# Run the function
data = asyncio.run(fetch_and_parse_data())
data_name = asyncio.run(name_by_id(data['paySystems']))
print(data_name)
data_id = asyncio.run(accept_ways_by_direction(data['toDirections'][4]))
print(data_id[4])
pprint(asyncio.run(dict_by_id(data_name, data_id[4])))
