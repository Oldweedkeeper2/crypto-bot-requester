import asyncio
import json
from pprint import pprint

import httpx


async def create_order(coin_from: str, coin_to: str, give: str, get: str, email: str, coin_from_wallet: str,
                       coin_to_wallet: str) -> None:
    options = {'address': f'{coin_to_wallet}'}
    options = json.dumps(options)
    data = {
        "source_amount": give,
        "destination_amount": get,
        "withdrawal[address]:": coin_to_wallet,
        'form_build_id': 'form-4Ns5FCbAPDHWJAYmxvY04WaduCAwdR7WmErBhHDBKKs',
        'form_token': 'PyMneTGPT3kDNwk013oJEyZLJlFEqzdY5f9AT-Xqrmo',
        'form_id': 'exchange_form_exchange_new',
        'promo_code': '',
        'op': ''}
    pprint(data)
    xml_data = httpx.post(f'https://www.alfa.cash/convert/{coin_from}/{coin_to}/{get}', data=data)
    pprint(xml_data.headers)


# pprint(asyncio.run(check_exchange_rates()))
pprint(asyncio.run(
        create_order(coin_from='bitcoin', coin_to='litecoin', give='4.953', get='6.431',
                     email='oleg-ermakov11@mail.ru', coin_from_wallet='',
                     coin_to_wallet='1FgThhtLdSM1i78vXHGovA3WxzbTWA2mse')))
