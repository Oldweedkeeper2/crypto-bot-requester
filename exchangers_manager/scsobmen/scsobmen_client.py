import asyncio

from playwright.async_api import async_playwright


async def create_order(coin_from: str, coin_to: str, give: str, email: str, coin_from_wallet: str) -> None:
    async with async_playwright() as p:
        browser_type = p.firefox
        browser = await browser_type.launch(headless=False, timeout=50000)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f'https://scsobmen.com/exchange-{coin_from}-to-{coin_to}/')


asyncio.run(create_order(coin_from='tron', coin_to='bitcoin', give='3500', email='orer-32weq@mail.ru',
                         coin_from_wallet='3F1tAaz5x1HUXrCNLbtMDqcw6o12Nn4xqX'))
