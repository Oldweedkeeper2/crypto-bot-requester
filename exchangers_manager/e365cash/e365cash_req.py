import asyncio
from pprint import pprint
from typing import Dict, List

from bs4 import BeautifulSoup
import httpx

from exchangers_manager.xml_parser import xml_parse


# проблема: забанен по ip на 15минут x2
# решение: использовать мобильные прокси

async def fetch_and_parse_data() -> List[Dict]:
    # Initialize an HTTP client
    client = httpx.Client()
    
    # Initialize an empty list to store the data
    data = []
    
    # Make a request to the main page
    r = client.get('https://365cash.co')
    
    # Parse the HTML content of the main page
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Find all 'li' elements with the attribute 'data-code'
    for li in soup.find_all('li', attrs={'data-code': True}):
        data_code = li.get('data-code')
        currency_name_element = li.find('a', class_='currency-name')
        currency_amount_element = li.find('p', class_='currency-amount')
        
        if currency_name_element and currency_amount_element:
            currency_amount = currency_amount_element.text
            href = currency_name_element.get('href')
            coin_from, coin_to = href.split('/')[1:]  # Assuming the href is in the format '/TRX/BTC'
            
            # Make a request to the exchange rate page
            r = client.get(f'https://365cash.co{href}')
            r.raise_for_status()
            
            # Parse the HTML content of the exchange rate page
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Find the course and min transaction
            course_element = soup.find('p', id='pre-order-form-course')
            min_transaction_element = soup.find('div', class_='hint-block')
            
            if course_element and min_transaction_element:
                course = course_element.find('span', attrs={'data-key': 'c'}).text
                min_transaction = min_transaction_element.text.split(' ')[
                    1]  # Assuming the min transaction is in the format 'От 50 до 9459.37 USD'
                
                # Append the data to the list as a dictionary
                data.append({
                    'from_currency': coin_from,
                    'to_currency': coin_to,
                    'exchange_rate': course,
                    'min_exchange_amount': min_transaction,
                    "reserve": None
                })
    
    # Close the HTTP client
    client.close()
    return data


# pprint(asyncio.run(fetch_and_parse_data()))
