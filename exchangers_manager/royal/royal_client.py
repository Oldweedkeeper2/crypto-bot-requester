import asyncio

from playwright.async_api import async_playwright

# работает
async def create_order(coin_from: str, coin_to: str, give: str, email: str, coin_from_wallet: str) -> str or tuple:
    async with async_playwright() as p:
        browser_type = p.firefox
        browser = await browser_type.launch(headless=False, timeout=50000)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f'https://royal.cash/lite/f1/buy/all/{coin_from}/all/{coin_to}/')
        await page.fill('input[type="text"]', give)
        await page.click('input[type="submit"]')
        await page.wait_for_timeout(5)
        await page.click('input[type="submit"]')
        await page.fill('input[name="email"]', email)
        await page.fill('input[name="to_acc"]', coin_from_wallet)
        await page.click('input[type="submit"]')
        requisites_list = await page.query_selector_all('[class="input"]')
        # example ['TDqMGjPzY1Jijkm7N6b9wxZQeSrBift2G9', '3500', '3F1tAaz5x1HUXrCNLbtMDqcw6o12Nn4xqX', '0.00934307']
        requisites = [await requisite.get_attribute('value') for requisite in requisites_list]
        await page.click('input[type="submit"]')
        return requisites[0]


asyncio.run(create_order(coin_from='tron', coin_to='bitcoin', give='3500', email='orer-32weq@mail.ru',
                         coin_from_wallet='3F1tAaz5x1HUXrCNLbtMDqcw6o12Nn4xqX'))
