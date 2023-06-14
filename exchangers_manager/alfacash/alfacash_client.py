import asyncio
import json
from pprint import pprint

import httpx
from playwright.async_api import async_playwright

# работает вроде бы
async def create_order(coin_from: str, coin_to: str, give: str, get: str, email: str, coin_from_wallet: str,
                       coin_to_wallet: str) -> str:
    async with async_playwright() as p:
        browser_type = p.firefox
        browser = await browser_type.launch(headless=False, timeout=50000)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f'https://www.alfa.cash/ru/exchange/{coin_from}/{coin_to}')
        await asyncio.sleep(4)
        if await page.query_selector('input[name="source_amount"]'):
            await page.type('input[name="source_amount"]', give)
        if await page.query_selector('input[name="withdrawal[address]"]'):
            await page.fill('input[name="withdrawal[address]"]', coin_to_wallet)
        await page.click('[class="custom-control-label"]')
        if await page.query_selector('input[name="source_amount"]'):
            await page.fill('input[name="source_amount"]', give)
        if await page.query_selector('input[id="edit-email"]'):
            await page.fill('input[id="edit-email"]', email)
        await asyncio.sleep(5)
        await page.click('[id="edit-submit"]')
        await asyncio.sleep(5)
        requisites = await page.query_selector('[id="copy-address-1"]')
        requisites = await requisites.inner_text()
        return requisites


# pprint(asyncio.run(check_exchange_rates()))
pprint(asyncio.run(
        create_order(coin_from='bitcoin', coin_to='litecoin', give='0.01', get='6.431',
                     email='', coin_from_wallet='',
                     coin_to_wallet='LZUU1kuoHp8iKLHfJB2NzPgVrx9rpnE4zi')))
