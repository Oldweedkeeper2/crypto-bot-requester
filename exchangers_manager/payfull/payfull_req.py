# wait ~10sec
import asyncio
from pprint import pprint
from typing import List, Dict

import httpx
from bs4 import BeautifulSoup

from manifests.tokens_manifest import Tokens

from playwright.async_api import async_playwright


# работает вроде как  (Кажется, Вы создаете и не оплачиваете слишком много заявок... Попробуйте позднее, либо обратитесь в чат.)
async def create_order(coin_from: str, coin_to: str, give: str, email: str, coin_from_wallet: str,
                       coin_to_wallet: str, fio='', phone='') -> str or None:
    # *convert*
    # coin_from = 36
    # coin_to = 337
    phone = '+7' + phone[1:] if phone.startswith('8') else phone
    async with async_playwright() as p:
        browser_type = p.firefox
        browser = await browser_type.launch(headless=False, timeout=50000)
        context = await browser.new_context()
        page = await context.new_page()
        print(f'https://payfull.ru/exchange-{coin_from}-to-{coin_to}/')
        await page.goto(f'https://payfull.ru/exchange-{coin_from}-to-{coin_to}/')

        # *check on fiat*
        # print(await page.query_selector('input[name="account1"]'))
        if await page.query_selector('input[name="account1"]'):
            await page.fill('input[name="account1"]', coin_from_wallet)
        if await page.query_selector('input[name="cf1"]'):
            await page.fill('input[name="cf1"]', fio)
        if await page.query_selector('input[name="cf4"]'):
            await page.fill('input[name="cf4"]', phone)
        await page.fill('input[name="sum1"]', give)
        await page.wait_for_timeout(5)
        await page.fill('input[name="cf6"]', email)
        await page.fill('input[id="account2"]', coin_to_wallet)

        await page.click('.xchange_checkdata_div.checkbox label')
        if await page.query_selector('input[type="submit"]'):
            await page.click('input[type="submit"]')
        # Wait for the button to appear in the popup
        await page.wait_for_selector('.standart_window_submit input[type="submit"]')

        # Click on the button
        
        await page.wait_for_timeout(2)
        if await page.query_selector('.ajax_post_bids_res'):
            error = await page.query_selector('.ajax_post_bids_res')
            return f'error with input data: {await error.inner_text()}'
        await page.wait_for_timeout(20)
        await asyncio.sleep(60)
        # await page.goto('https://payfull.ru/hst_Ijfkuhc07T6oyn2fhIXqkBApULa6MqDSyfo/')
        requisites = await page.query_selector_all('[class="xchange-steps__datalist-item-1"]')
        requisites = [await requisite.inner_text() for requisite in requisites]
        print(requisites)
        return requisites


asyncio.run(create_order(coin_from='QWRUB', coin_to='BTC', give='6500', email='orer-32weq@mail.ru',
                         coin_from_wallet='+79102795043',
                         coin_to_wallet='3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy', phone='89102795049',
                         fio='Эрминго Олхеус Миро'))

# xtt4_one_line_name
