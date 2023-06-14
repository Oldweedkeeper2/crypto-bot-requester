import asyncio
from pprint import pprint
from typing import List, Dict

from playwright.async_api import async_playwright

from manifests.exchangers_manifest import Exchangers
from manifests.tokens_manifest import Tokens



# работает
async def create_order(coin_from: str, coin_to: str, give: str, email: str, coin_from_wallet: str,
                       coin_to_wallet: str, fio='', phone='') -> List[Dict]:
    """
    function from parsing coin couples bestchange.ru
    :param coin_from:
    :param coin_to:
    :return List[Dict]:
    """
    # Connect to playwright sesscion
    async with async_playwright() as p:
        browser_type = p.firefox
        browser = await browser_type.launch(headless=False, timeout=50000)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f'https://365cash.co/{coin_from}/{coin_to}')
        if await page.query_selector('input[name="SellForm[sell_amount]"]'):
            await page.fill('input[name="SellForm[sell_amount]"]', give)
        
        if await page.query_selector('input[name="SellForm[sell_source]"]'):
            await page.fill('input[name="SellForm[sell_source]"]', coin_from_wallet)
        if await page.query_selector('input[name="BuyForm[buy_target]"]'):
            await page.fill('input[name="BuyForm[buy_target]"]', coin_to_wallet)
        
        await page.click('button[class="btn"]')
        await page.wait_for_timeout(20)
        await page.click('button[class="btn"]')
        await page.fill('input[name="cf6"]', email)
        await page.fill('input[name="account2"]', coin_to_wallet)
        # await page.click('input[type="submit"]')
        await page.check('input[name="check_data"]')
        input()
        await page.click('input[type="submit"]')
        input()
        
        
asyncio.run(create_order(coin_from='QWRUB', coin_to='BTC', give='16000', email='orer-32weq@mail.ru',
                         coin_from_wallet='+79102795043',
                         coin_to_wallet='1N4Qbzg6LSXUXyXu2MDuGfzxwMA7do8AyL', phone='89102795049',
                         fio='Эрминго Олхеус Миро'))