# 'https://mine.exchange/exchange_USDTERC20_to_CPTSRUB/'
import asyncio

from playwright.async_api import async_playwright

# просто не хочет работать почему-то
async def create_order(coin_from: str, coin_to: str, give: str, email: str, coin_from_wallet: str,
                       coin_to_wallet: str) -> str or tuple:
    async with async_playwright() as p:
        browser_type = p.firefox
        browser = await browser_type.launch(headless=False, timeout=50000)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f'https://mine.exchange/exchange_{coin_from}_to_{coin_to}/')
        await page.fill('input[name="sum1"]', give)
        if await page.query_selector('input[id="account1"]'):
            await page.fill('input[id="account1"]', coin_from_wallet)
        
        input()
        await page.wait_for_timeout(5)
        await page.fill('input[name="cf6"]', email)
        await page.fill('input[name="account2"]', coin_to_wallet)
        # await page.click('input[type="submit"]')
        await page.check('input[name="check_data"]')
        input()
        await page.click('input[type="submit"]')
        input()
        # payment = await page.query_selector('a[class="success_paybutton"]')
        # href = await payment.get_attribute('href')
        # return href


asyncio.run(
    create_order(coin_from='BTC', coin_to='CARDRUB', give='0.001', email='oleg-ermakov12@mail.ru', coin_from_wallet='1q6pk7gmdvyc48f3j95f3s6mmldvwj6e4wkvp2rjyg5drfr5az3xs2j2pqd',
                 coin_to_wallet='2200334452384000'))

