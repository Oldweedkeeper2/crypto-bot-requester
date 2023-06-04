import asyncio

import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


async def fetch_and_parse_data():
    parsed_data = []
    
    async with httpx.AsyncClient() as client:
        response = await client.get('https://netex24.net/api/exchangeDirection/getAll')
        print(response.text)
    # soup = BeautifulSoup(response.text, 'html.parser')
    #
    # # Find the HTML elements that contain the data
    # # This is just a placeholder, you'll need to replace it with the actual criteria
    # data_elements = soup.find_all('div', class_='data-element')
    #
    # for element in data_elements:
    #     # Extract the data from the element
    #     # This is just a placeholder, you'll need to replace it with the actual criteria
    #     coin_names = element.find('div', class_='tarif_curs_title_ins').text
    #     give_get = float(element.find('div', class_='tarif_curs').text)
    #
    #     # Append the data to the list as a dictionary
    #     parsed_data.append({
    #         'from:': coin_names[0],
    #         'to:': coin_names[1],
    #         'give:': give_get[0],
    #         'get:': give_get[1],
    #     })
    #
    # return parsed_data


async def track_a_couple():
    # Connect to playwright sesscion
    async with async_playwright() as p:
        browser_type = p.firefox
        browser = await browser_type.launch(headless=False, timeout=50000)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f'https://netex24.net/#/ru/tariffs')
        input()

# Run the function
data = asyncio.run(track_a_couple())
print(data)
