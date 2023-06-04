import asyncio
import json
from pprint import pprint
from typing import List, Dict
import httpx
from playwright.async_api import async_playwright

from manifests.exchangers_manifest import Exchangers
from manifests.tokens_manifest import Tokens
from alfabit_req import *


# check how to accept transaction
async def create_order(uid, coin_from_wallet, coin_to_wallet) -> str:
    async with async_playwright() as p:
        browser_type = p.firefox
        browser = await browser_type.launch(headless=False, timeout=50000)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f'https://alfabit.org/ru/order/{uid}')
        input()
        try:
            await page.wait_for_timeout(10)
            requisites = await page.query_selector_all('dd[class="ui-property__text"]')
            for requisite in requisites:
                requisite = await requisite.inner_text()
            print(requisite)
            input()
        except:
            return None
        return requisite


async def proof_of_payment(uid, coin_from_wallet, coin_to_wallet) -> None:
    async with async_playwright() as p:
        browser_type = p.firefox
        browser = await browser_type.launch(headless=False, timeout=50000)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f'https://alfabit.org/ru/order/{uid}')
        await page.wait_for_timeout(10)
        await page.click('[class="ui-button ui-button--filled_primary actions__action"]')
        input()


async def create_transaction(coin_from: str, coin_to: str, give: float, get: float, coin_from_wallet: str,
                             coin_to_wallet: str, email: str, token: str):
    xml_data = await check_exchange_rate(coin_from, coin_to)
    if xml_data['min_money1'] > give:
        return f'min_exchange: {xml_data["min_money1"]}'
    rate = xml_data['exchange_rate']
    print(rate)
    data = {'amount_money1': give,
            'amount_money2': get,
            'comment': "",
            'email': email,
            'lang': "ru",
            'money1': coin_from,
            'money2': coin_to,
            'rate': rate,
            'req_money1': coin_from_wallet,
            'req_money2': coin_to_wallet,
            'rid': "",
            'token': token}
    
    xml_data = httpx.post('https://alfabit.org/api/v1/order/create/', data=data)
    xml_data = json.loads(xml_data.text)
    print(xml_data)
    return xml_data['uid']


# {"id":634874,"uid":"26c9a372-5b31-4476-a321-306ccfa89e3d","email":"oleg-ermakov11@mail.ru","money1":"USD Coin(USDC)","money2":"Сбербанк(RUB)","money2_memo_tag":null,"req_money1":"none","req_money2":"4222322332232323","amount_money1":"1487.06","amount_money2":"122131.84","status":0,"date_make_order":1685440459.792457,"client_comment":""}

if __name__ == '__main__':
    coin_from = 'Tether(USDT) ERC20'
    coin_to = 'Bitcoin(BTC)'
    give = 100
    get = 0.003662439
    coin_from_wallet = ''
    coin_to_wallet = '1N4Qbzg6LSXUXyXu2MDuGfzxwMA7do8AyL'
    email = 'mesinos280@onlcool.com'
    token = 'wNxNg6B5FDxHe4s5ExULd41d7ec8Dx'
    uid = asyncio.run(
            create_transaction(coin_from=coin_from, coin_to=coin_to, give=give, get=get,
                               coin_from_wallet=coin_from_wallet, coin_to_wallet=coin_to_wallet,
                               email=email, token=token))
    if not uid.startswith('min_exchange'):
        requisites = asyncio.run(create_order(uid, coin_from_wallet, coin_to_wallet))
        if requisites is not None:
            proof_of_payment = asyncio.run(proof_of_payment(uid, coin_from_wallet, coin_to_wallet))

#     data = {'amount_money1': 70,
#             'amount_money2': 121.6278,
#             'comment': "",
#             'email': "oleg-ermakov11@mail.ru",
#             'lang': "ru",
#             'money1': "WAVES",
#             'money2': "Tether(USDT) TRC20",
#             'rate': 1.73754,
#             'req_money1': "2131221442121323322",
#             'req_money2': "2131234123122451322",
#             'rid': "",
#             'token': "wNxNg6B5FDxHe4s5ExULd41d7ec8Dx"}
# {
#     'amount_money1': 2018.77,
#     'amount_money2': 0.070198147,
#     'comment': "",
#     'email': "oleg-ermakov11@mail.ru",
#     'lang': "ru",
#     'money1': "Tether(USDT) BEP20",
#     'money2': "Bitcoin(BTC)",
#     'rate': 28758.17,
#     'req_money1': "",
#     'req_money2': "3F1tAaz5x1HUXrCNLbtMDqcw6o12Nn4xqX",
#     'rid': "",
#     'token': "wNxNg6B5FDxHe4s5ExULd41d7ec8Dx"}
