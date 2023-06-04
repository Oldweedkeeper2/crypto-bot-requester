import asyncio

from playwright.async_api import async_playwright


# convert name into indexes
async def create_order(coin_from: str, coin_to: str, give: str, email: str, coin_from_wallet: str,
                       coin_to_wallet: str, fio='', phone='') -> str or None:
    # *convert*
    # coin_from = 36
    # coin_to = 337
    coin_to_id = 32
    phone = '+7' + phone[1:] if phone.startswith('8') else phone
    async with async_playwright() as p:
        browser_type = p.firefox
        browser = await browser_type.launch(headless=False, timeout=50000)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f'https://expochange.org/xchange_{coin_from}_to_{coin_to}/')

        await page.fill('[name="summ1"]', give)
        await page.click('[name="summ1"]')
        if await page.query_selector('[name="wschet1"]'):
            await page.fill('[name="wschet1"]', coin_from_wallet)
        if await page.query_selector('[name="wschet2"]'):
            await page.fill('[name="wschet2"]', coin_to_wallet)
        if await page.query_selector('[name="user_email"]'):
            await page.fill('[name="user_email"]', email)
        if await page.query_selector('[name="first_name"]'):
            await page.fill('[name="first_name"]', 'балбес')
        if await page.query_selector('[name="cfc3"]'):
            await page.fill('[name="cfc3"]', fio)
        await page.click('.xchangestep1submit > input')
        await page.wait_for_timeout(20)
        await page.check('[class="amlcheck"]')
        check = await page.query_selector('[class="check"]')
        order_field = await check.query_selector_all('[class="col-lg-7 text-check2"]')
        order = [await row.inner_text() for row in order_field]
        order_field_add = await page.query_selector_all('[class="col-lg-7 text-check2 schet"]')
        order_add = [await row.inner_text() for row in order_field_add]
        order.extend(order_add)
        print(order)
        input()
        await page.click('input[id="createzaja"]')
        await page.wait_for_timeout(20)
        requisite = await page.query_selector('span[id="card"]')
        summ = await page.query_selector('span[id="sum"]')
        requisites = {'requisite': await requisite.inner_text(), 'summ': await summ.inner_text()}
        print(requisites)
        input()
        await page.click('[name="payed"]')
        input()


asyncio.run(create_order(coin_from='QWRUB', coin_to='BTC', give='6500', email='orer-32weq@mail.ru',
                         coin_from_wallet='+79102795043',
                         coin_to_wallet='3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy', phone='89102795049',
                         fio='Эрминго Олхеус Миро'))
# LTC, SBERRUB
# card, BTC
