import asyncio

from playwright.async_api import async_playwright

# капча
async def create_order(coin_from: str, coin_to: str, give: str, email: str, coin_from_wallet: str,
                       coin_to_wallet: str, phone: str = None, name: str = None, surname: str = None) -> None:
    async with async_playwright() as p:
        browser_type = p.firefox
        browser = await browser_type.launch(headless=False, timeout=50000)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f'https://scsobmen.com/exchange-{coin_from}-to-{coin_to}/')
        if page.query_selector('[name="sum1"]'):
            await page.fill('[name="sum1"]', give)
        if page.query_selector('[name="account1"]'):
            await page.fill('[name="account1"]', coin_from_wallet)
        if page.query_selector('[name="cfgive3"]'):
            await page.fill('[name="cfgive3"]', phone)
        if page.query_selector('[name="account2"]'):
            await page.fill('[name="account2"]', coin_to_wallet)
        if page.query_selector('[name="cf1"]'):
            await page.fill('[name="cf1"]', name)
        if page.query_selector('[name="cf2"]'):
            await page.fill('[name="cf2"]', surname)
        if page.query_selector('[name="cf6"]'):
            await page.fill('[name="cf6"]', email)


asyncio.run(create_order(coin_from='tron', coin_to='bitcoin', give='3500', email='orer-32weq@mail.ru',
                         coin_from_wallet='3F1tAaz5x1HUXrCNLbtMDqcw6o12Nn4xqX'))
