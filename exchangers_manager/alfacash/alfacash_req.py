import asyncio
import json
from pprint import pprint
from typing import Dict, List

import httpx

from exchangers_manager.xml_parser import xml_parse


async def check_exchange_rates() -> List[Dict]:
    xml_data = httpx.get('https://www.alfa.cash/api/rates')
    parsed_xml_data = await xml_parse(xml_data.text)
    
    return parsed_xml_data


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

# https://www.alfa.cash/api/status/[secret_key]

# source_amount: 0.03388821
# destination_amount: 0.00194943
# withdrawal[address]: 1FgThhtLdSM1i78vXHGovA3WxzbTWA2mse
# promo_code:
# accept_rules: 1
# op:
# promo_code_discount:
# promo_code_include_user_discount:
# form_build_id: form-4Ns5FCbAPDHWJAYmxvY04WaduCAwdR7WmErBhHDBKKs
# form_token: PyMneTGPT3kDNwk013oJEyZLJlFEqzdY5f9AT-Xqrmo
# form_id: exchange_form_exchange_new
# {
# "gate_deposit": "Пример: 'биткоин'. Столбец ворот из Направления обмена",
# "gate_withdrawal": "Пример: 'litecoin'. Столбец ворот из Направления обмена",
# "pair": "[УСТАРЕЛО] Пример: 'BTC_LTC'. Направление обмена, заданное в форме [исходный_код_валюты]_[целевой_код_валюты].",
# "deposit_amount": "(Необязательно) пример: '4.953', фиксированная сумма депозита, которую вы хотите отправить на обмен.",
# "withdrawal_amount": "(Необязательно) пример: '6.431', фиксированная сумма вывода, которую вы хотите получить после совершения обмена.",
# "email": "Пример: 'email@example.com'",
# "options": "Пример: {'address': '1FgThhtLdSM1i78vXHGovA3WxzbTWA2mse'}, этот массив параметров зависит от source_currency_code.",
# "r_uid": "(Необязательно) пример: '2f777791', идентификатор партнерской программы.",
# "promo_code": "(Необязательно) пример: 'ALFACODE'."
# }
