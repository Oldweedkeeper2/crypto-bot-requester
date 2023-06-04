import asyncio
from pprint import pprint

import httpx
from bs4 import BeautifulSoup

from manifests.exchangers_manifest import Exchangers
from manifests.tokens_manifest import Tokens


# забанен на ip


async def fetch_and_parse_data():
    parsed_data = []
    
    async with httpx.AsyncClient() as client:
        response = await client.get('https://myxa.cc/tarifs/')
        response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the HTML elements that contain the data
    coin_names = soup.find_all('div', class_='tarif_curs_title_ins')
    coin_names = list(map(lambda x: x.text.replace('\n', ''), coin_names))
    give_get = soup.find_all('div', class_='tarif_curs_ins')
    give_get = list(map(lambda x: x.text.replace('\xa0', ' ').replace(' ', ''), give_get))
    
    coin_from = [give_get[x].split('\n')[3] for x in range(1, len(give_get), 2)]
    coin_to = [give_get[x].split('\n')[3] for x in range(0, len(give_get), 2)]
    give = [give_get[x].split('\n')[1] for x in range(0, len(give_get), 2)]
    get = [give_get[x].split('\n')[1] for x in range(1, len(give_get), 2)]
    
    grouped_data = []
    for index, values in enumerate(zip(coin_from, coin_to, give, get)):
        if values[0] in Tokens.tokens_ABB:  # Append only needed exchangers
            try:
                exchange_rate = float(values[2]) / float(values[3])
            except (ValueError, ZeroDivisionError):
                exchange_rate = None
                
            if exchange_rate is None:
                formatted_exchange_rate = None
            else:
                formatted_exchange_rate = "{:.8f}".format(exchange_rate)
            group_dict = {
                'from:': values[0],
                'to:': values[1],
                'give:': values[2],
                'get:': values[3]
            }
            myxa_data = {
                "from_currency": values[0],
                "to_currency": values[1],
                "exchange_rate": formatted_exchange_rate,
                "min_exchange_amount": None,  # This field doesn't exist in the Myxa format
                "reserve": None  # This field doesn't exist in the Myxa format
            }
            grouped_data.append(myxa_data)
    
    return grouped_data


# Run the function
data = asyncio.run(fetch_and_parse_data())
pprint(data)
