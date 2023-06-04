# https://myxa.cc/exchange_prusd_to_kspbkzt3/
import asyncio

from playwright.async_api import async_playwright


async def create_order(coin_from: str, coin_to: str, give: str, email: str, coin_from_wallet: str,
                       coin_to_wallet: str) -> str or tuple:
    async with async_playwright() as p:
        browser_type = p.firefox
        browser = await browser_type.launch(headless=False, timeout=50000)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f'https://royal.cash/lite/f1/buy/all/{coin_from}/all/{coin_to}/')
        await page.fill('input[name="account1"]', coin_to_wallet)
        await page.fill('input[name="sum1"]', give)
        await page.wait_for_timeout(5)
        await page.fill('input[name="cf6"]', email)
        await page.fill('input[name="account2"]', coin_from_wallet)
        await page.click('input[type="submit"]')
        await page.check('[class="checkbox"]')
        await page.click('input[type="submit"]')
        payment = await page.query_selector('a[class="success_paybutton"]')
        href = await payment.get_attribute('href')
        return href
        # href = 'https://merch.g-24.pro/?lang=ru&amount=50000&type=btc2btc&destAccount=bc1qx6l577n6un27ng0wjdkn5tc5v6d27g5jaxw90p&order=759700&callbackUrl=https:%2F%2Fmyxa.cc%2Fhst_GnpDujAVlHL5ADTgKbPC84tJQwXFnIVnO7a%2F&expire=1685744063'


async def proof_order(href: str) -> None:
    async with async_playwright() as p:
        browser_type = p.firefox
        browser = await browser_type.launch(headless=False, timeout=50000)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f'{href}')
        await page.click('mat-checkbox[id="mat-checkbox-2"]')
        await page.click('button[class="mat-focus-indicator mat-raised-button mat-button-base"]')
        requisite_field = await page.query_selector('[class="address"]')
        requisite = (await requisite_field.inner_text()).replace('content_copy', '')
        summ_field = await page.query_selector('[class="amount"]')
        summ = (await summ_field.inner_text()).replace('content_copy', '')
        print(requisite, summ)
        input()
        await page.click('mat-checkbox[id="mat-checkbox-1"]')
        input()
        
        await page.click('button[class="mat-focus-indicator mat-raised-button mat-button-base mat-button-disabled"]')
        input()


asyncio.run(create_order(coin_from='tron', coin_to='bitcoin', give='3500', email='orer-32weq@mail.ru',
                         coin_from_wallet='3F1tAaz5x1HUXrCNLbtMDqcw6o12Nn4xqX',
                         coin_to_wallet='372137123yweqg87612trsad'))
