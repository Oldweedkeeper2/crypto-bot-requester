import requests
import zipfile
import io
import codecs
from operator import itemgetter

from manifests.exchangers_manifest import Exchangers
from manifests.tokens_manifest import Tokens


class Rates:
    # Download the zip file
    response = requests.get('http://api.bestchange.ru/info.zip')
    zip_content = io.BytesIO(response.content)
    
    # Open the zip file
    zip_file = zipfile.ZipFile(zip_content)
    
    # Read and decode the files
    currencies = {}
    for line in codecs.iterdecode(zip_file.open('bm_cy.dat'), 'windows-1251'):
        entry = line.strip().split(';')
        if len(entry) > 2:
            currencies[entry[0]] = entry[2]
    
    exchangers = {}
    for line in codecs.iterdecode(zip_file.open('bm_exch.dat'), 'windows-1251'):
        entry = line.strip().split(';')
        if len(entry) > 1:
            exchangers[entry[0]] = entry[1]
    
    rates = {}
    for line in codecs.iterdecode(zip_file.open('bm_rates.dat'), 'windows-1251'):
        entry = line.strip().split(';')
        if len(entry) > 6:
            if entry[0] not in rates:
                rates[entry[0]] = {}
            if entry[1] not in rates[entry[0]]:
                rates[entry[0]][entry[1]] = {}
            rates[entry[0]][entry[1]][entry[2]] = {
                'rate': float(entry[3]) / float(entry[4]),
                'reserve': entry[5],
                'reviews': entry[6].replace('.', '/')
            }
    
    # Close the zip file
    zip_file.close()
    
    exch_ids = {}
    # # Print the exchanger list
    for exch_id, exch_name in sorted(exchangers.items()):
        if exch_name in Exchangers.exchangers_valid_name:
            exch_ids[exch_id] = exch_name
            # print(f"{exch_id} - {exch_name}")
    
    cy_ids = {}
    # Print the currency list
    for cy_id, cy_name in sorted(currencies.items()):
        if cy_name.split(' ')[-1].strip('()') in Tokens.tokens_ABB:
            cy_name_all = cy_name.replace('(', '').replace(')', '').split(' ')
            cy_name_new = ' '.join(cy_name_all[:-1])
            cy_ids[tuple([cy_name_new, cy_name_all[-1]])] = cy_id
            # print(f"{cy_id} - {cy_name}")
    
    print("\nExchanger list:")
    print(exch_ids)
    
    print("\nCurrency list:")
    print(cy_ids)


def get_best_currency_rate(token_from: str, token_to: str, chain_from: str, chain_to: str):
    from_cy = ''
    to_cy = ''
    for token in Rates.cy_ids:
        if token_from in token and chain_from in token:
            from_cy = Rates.cy_ids[token]
            break
    for token in Rates.cy_ids:
        if token_to in token and chain_to in token:
            to_cy = Rates.cy_ids[token]
            break
    
    sorted_rates = sorted(Rates.rates[from_cy][to_cy].items(), key=lambda x: x[1]['rate'])
    
    best_rates = []
    for exch_id, entry in sorted_rates:
        if exch_id in Rates.exch_ids:
            best_rates.append({'exchange_name': Rates.exchangers[exch_id],
                               'reviews': entry['reviews'],
                               'currency_from': Rates.currencies[from_cy],
                               'currency_to': Rates.currencies[to_cy],
                               'reserve': entry['reserve']})
            # print(
            #         f"{Rates.exchangers[exch_id]} - reviews {entry['reviews']} - rate {entry['rate']} {Rates.currencies[from_cy]} -> {Rates.currencies[to_cy]} - reserve {entry['reserve']} {Rates.currencies[to_cy]}")
    
    return best_rates[-1]


q = get_best_currency_rate(token_from='BTC', token_to='USDT', chain_from='Bitcoin', chain_to='Tether TRC20')
print(q)
# {'exchange_name': 'PayFull', 'reviews': '0/1767', 'currency_from': 'Bitcoin (BTC)', 'currency_to': 'Tether TRC20 (USDT)', 'reserve': '250000'}


# {'items_to_del': [61], 'trade_type': 'single', 'message_id': 61, 'chat_id': 426182274, 'network': 'ethereum',
# 'chain_id': '1', 'token': 'eth', 'withdrawal_method': 'crypto', 'withdrawal_network': 'binance-smart-chain',
# 'withdrawal_chain_id': '2', 'withdrawal_token': 'usdt'}
