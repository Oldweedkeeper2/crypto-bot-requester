import asyncio
from pprint import pprint

import httpx
from bs4 import BeautifulSoup


# doesn`t work, locked api
async def fetch_and_parse_data():
    parsed_data = []
    
    async with httpx.AsyncClient() as client:
        response = await client.get('https://izibtc.net/')
        response.raise_for_status()
        pprint(response.text)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the HTML elements that contain the data
    # This is just a placeholder, you'll need to replace it with the actual criteria
    data_elements = soup.find_all('div', class_='data-element')
    
    for element in data_elements:
        # Extract the data from the element
        # This is just a placeholder, you'll need to replace it with the actual criteria
        from_currency = element.find('div', class_='from-currency').text
        to_currency = element.find('div', class_='to-currency').text
        give = 1
        get = float(element.find('div', class_='get').text)
        amount = float(element.find('div', class_='amount').text)
        minamount = float(element.find('div', class_='minamount').text)
        
        # Append the data to the list as a dictionary
        parsed_data.append({
            'from:': from_currency,
            'to:': to_currency,
            'give:': give,
            'get:': get,
            'amount:': amount,
            'minamount': minamount
        })
    
    return parsed_data


# Run the function
data = asyncio.run(fetch_and_parse_data())
print(data)
data1 = {'direction_from': 161,
         'direction_to': 44,
         'is_from': False}
r = httpx.post('https://izibtc.net/dir/get?direction_from=68&direction_to=44&is_from=true')
print(r.text)
