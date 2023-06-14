import asyncio
import time
from pprint import pprint
from typing import Any, Coroutine

import requests
import zipfile
import io
import codecs
from operator import itemgetter

from manifests.exchangers_manifest import Exchangers
from manifests.tokens_manifest import Tokens


class Rates:
    def __init__(self):
        self.currencies = {}
        self.exchangers = {}
        self.rates = {}
        self.exch_ids = {}
        self.cy_ids = {}
        
        # self.download_and_process_data()
    
    async def download_and_process_data(self):
        # Download the zip file
        response = requests.get('http://api.bestchange.ru/info.zip')
        zip_content = io.BytesIO(response.content)
        
        # Open the zip file
        with zipfile.ZipFile(zip_content) as zip_file:
            await self.process_files(zip_file)
    
    async def process_files(self, zip_file: {open}):
        await self.process_currencies(zip_file)
        await self.process_exchangers(zip_file)
        await self.process_rates(zip_file)
        await self.process_currencies_our()
        await self.process_exchangers_our()
    
    async def process_currencies(self, zip_file: {open}):
        for line in codecs.iterdecode(zip_file.open('bm_cy.dat'), 'windows-1251'):
            entry = line.strip().split(';')
            if len(entry) > 2:
                self.currencies[entry[0]] = entry[2]
    
    async def process_exchangers(self, zip_file: {open}):
        for line in codecs.iterdecode(zip_file.open('bm_exch.dat'), 'windows-1251'):
            entry = line.strip().split(';')
            if len(entry) > 1:
                self.exchangers[entry[0]] = entry[1]
    
    async def process_rates(self, zip_file: {open}):
        for line in codecs.iterdecode(zip_file.open('bm_rates.dat'), 'windows-1251'):
            entry = line.strip().split(';')
            # print(entry)
            if len(entry) > 6:
                if entry[0] not in self.rates:
                    self.rates[entry[0]] = {}
                if entry[1] not in self.rates[entry[0]]:
                    self.rates[entry[0]][entry[1]] = {}
                self.rates[entry[0]][entry[1]][entry[2]] = {
                    'rate': float(entry[3]) / float(entry[4]),
                    'reserve': entry[5],
                    'reviews': entry[6].replace('.', '/'),
                    'minamount': entry[8],
                    'maxamount': entry[9]
                }
        # print(self.rates)
    
    async def process_currencies_our(self):
        # Print the currency list
        for cy_id, cy_name in list(
                filter(lambda x: x[1].split(' ')[-1].strip('()') in Tokens.tokens_ABB,
                       sorted(self.currencies.items()))):
            cy_name_all = cy_name.replace('(', '').replace(')', '').split(' ')
            cy_name_new = ' '.join(cy_name_all[:-1])
            self.cy_ids[tuple([cy_name_new, cy_name_all[-1]])] = cy_id
    
    async def process_exchangers_our(self):
        # # Print the exchanger list
        for exch_id, exch_name in list(
                filter(lambda x: x[1] in Exchangers.exchangers_valid_name, sorted(self.exchangers.items()))):
            self.exch_ids[exch_id] = exch_name
            # print(f"{exch_id} - {exch_name}")
    
    async def get_best_currency_rate(self, token_from: str, token_to: str, chain_from: str, chain_to: str,
                                     amount: float):
        
        from_cy, to_cy = '', ''
        for token in self.cy_ids:
            if token_from in token and chain_from in token:
                from_cy = self.cy_ids[token]
            if token_to in token and chain_to in token:
                to_cy = self.cy_ids[token]
            if from_cy and to_cy:
                break
        if not (from_cy or to_cy):
            return None
        try:
            sorted_rates = sorted(self.rates[from_cy][to_cy].items(), key=lambda x: x[1]['rate'])
        except Exception as e:
            print(e)
            return None
        best_rates = []
        for exch_id, entry in sorted_rates:
            if exch_id in self.exch_ids:
                best_rates.append({'exchange_name': self.exchangers[exch_id],
                                   'reviews': entry['reviews'],
                                   'currency_from': self.currencies[from_cy],
                                   'currency_to': self.currencies[to_cy],
                                   'rate': entry['rate'],
                                   'reserve': entry['reserve'],
                                   'minamount': entry['minamount'],
                                   'maxamount': entry['maxamount']})
        
        best_rates = list(
                filter(lambda x: float(x['minamount']) <= amount < float(x['maxamount']), best_rates))
        # print(float(best_rates[0]['rate']),amount,float(best_rates[0]['maxamount']))
        print(best_rates)
        return best_rates[-1] if best_rates else None
    
    async def get_double_exchange_rate(self, token_from: str, token_to: str, chain_from: str, chain_to: str):
        from_cy, to_cy, inter_cy = '', '', ''
        for token in self.cy_ids:
            if token_from in token and chain_from in token:
                from_cy = self.cy_ids[token]
            if token_to in token and chain_to in token:
                to_cy = self.cy_ids[token]
            
            if from_cy and to_cy:
                break
        
        sorted_rates_from_inter = sorted(self.rates[from_cy][to_cy].items(), key=lambda x: x[1]['rate'])
        sorted_rates_inter_to = sorted(self.rates[to_cy][from_cy].items(), key=lambda x: x[1]['rate'])
        
        rates_from = []
        rates_to = []
        for exch_id, entry in sorted_rates_from_inter:
            if exch_id in self.exch_ids:
                rates_from.append({'exchange_name': self.exchangers[exch_id],
                                   'reviews': entry['reviews'],
                                   'currency_from': self.currencies[from_cy],
                                   'currency_to': self.currencies[to_cy],
                                   'rate': entry['rate'],
                                   'reserve': entry['reserve']})
        
        for exch_id, entry in sorted_rates_inter_to:
            if exch_id in self.exch_ids:
                rates_to.append({'exchange_name': self.exchangers[exch_id],
                                 'reviews': entry['reviews'],
                                 'currency_from': self.currencies[from_cy],
                                 'currency_to': self.currencies[to_cy],
                                 'rate': entry['rate'],
                                 'reserve': entry['reserve']})
        
        return rates_from, rates_to if rates_from and rates_to else None
    
    async def get_best_rates_from(self, token_from: str, chain_from: str, amount: float):
        from_cy = ''
        for token in self.cy_ids:
            if token_from in token and chain_from in token:
                from_cy = self.cy_ids[token]
                break
        if not from_cy:
            return None
        
        best_rates = []
        for to_cy in self.rates[from_cy]:
            try:
                sorted_rates = sorted(self.rates[from_cy][to_cy].items(), key=lambda x: x[1]['rate'])
            except Exception as e:
                print(e)
                continue
            
            for exch_id, entry in sorted_rates:
                if exch_id in self.exch_ids:
                    best_rates.append({
                        'exchange_name': self.exchangers[exch_id],
                        'reviews': entry['reviews'],
                        'currency_from': self.currencies[from_cy],
                        'currency_to': self.currencies[to_cy],
                        'rate': entry['rate'],
                        'reserve': entry['reserve'],
                        'minamount': entry['minamount'],
                        'maxamount': entry['maxamount']
                    })
        
        best_rates = list(
                filter(lambda x: float(x['minamount']) <= amount < float(x['maxamount']), best_rates))
        
        return best_rates
    
    async def get_best_rates_to(self, token_to: str, chain_to: str, amount: float):
        to_cy = ''
        for token in self.cy_ids:
            if token_to in token and chain_to in token:
                to_cy = self.cy_ids[token]
                break
        if not to_cy:
            return None
        
        best_rates = []
        for from_cy in self.currencies:
            if from_cy not in self.rates or to_cy not in self.rates[from_cy]:
                continue
            try:
                sorted_rates = sorted(self.rates[from_cy][to_cy].items(), key=lambda x: x[1]['rate'])
            except Exception as e:
                print(e)
                continue
            
            for exch_id, entry in sorted_rates:
                if exch_id in self.exch_ids:
                    best_rates.append({
                        'exchange_name': self.exchangers[exch_id],
                        'reviews': entry['reviews'],
                        'currency_from': self.currencies[from_cy],
                        'currency_to': self.currencies[to_cy],
                        'rate': entry['rate'],
                        'reserve': entry['reserve'],
                        'minamount': entry['minamount'],
                        'maxamount': entry['maxamount']
                    })
        
        best_rates = list(
                filter(lambda x: float(x['minamount']) <= amount < float(x['maxamount']), best_rates))
        
        return best_rates
    
    async def find_best_double_exchange_path(self,best_rates_from, best_rates_to):
        # Create sets of the 'currency_to' values in each list
        currencies_from = set(rate['currency_to'] for rate in best_rates_from)
        currencies_to = set(rate['currency_from'] for rate in best_rates_to)
        
        # Find the intersection of the two sets
        common_currencies = currencies_from & currencies_to
        
        # If there are no common currencies, there is no possible double exchange path
        if not common_currencies:
            return None
        
        # Find the best rates for the common currencies
        best_from_rates = [rate for rate in best_rates_from if rate['currency_to'] in common_currencies]
        best_to_rates = [rate for rate in best_rates_to if rate['currency_from'] in common_currencies]
        
        # Sort the lists by rate
        best_from_rates.sort(key=lambda rate: rate['rate'], reverse=True)
        best_to_rates.sort(key=lambda rate: rate['rate'], reverse=True)
        
        # The best path is the one with the highest combined rate
        best_path = None
        best_combined_rate = 0
        c = []
        for currency in common_currencies:
            from_rate = next((rate for rate in best_from_rates if rate['currency_to'] == currency), None)
            to_rate = next((rate for rate in best_to_rates if rate['currency_from'] == currency), None)
            
            if from_rate and to_rate:
                combined_rate = from_rate['rate'] * to_rate['rate']
                c.append(combined_rate)
                if combined_rate > best_combined_rate:
                    best_combined_rate = combined_rate
                    best_path = [from_rate, to_rate]
                    
        return best_path
# спросить в каком формате выводить

# pprint(rates.currencies) # вот тут все форматы валют, просто включи
# pprint(rates.exchangers)
# pprint(rates.cy_ids)
# pprint(rates.exch_ids)

async def exchange_hub(token_from: str, token_to: str, chain_from: str, chain_to: str,
                       amount: float):
    rates = Rates()
    await rates.download_and_process_data()
    best = await rates.get_best_currency_rate(token_from, token_to, chain_from, chain_to,
                                              amount)
    return (best['exchange_name'], '{:.16f}'.format(
            amount / float(best['rate']))) if best else None  # '{:.16f}'.format - число знаков после запятой


async def exchange_hub_double(token_from: str, token_to: str, chain_from: str, chain_to: str,
                              amount: float):
    rates = Rates()
    await rates.download_and_process_data()
    token_from_rates = await rates.get_best_rates_from(token_from=token_from, chain_from=chain_from, amount=amount)
    pprint(token_from_rates)
    await rates.download_and_process_data()
    token_to_rates = await rates.get_best_rates_to(token_to=token_to, chain_to=chain_to, amount=amount)
    pprint(token_to_rates)
    total_rate = await rates.find_best_double_exchange_path(best_rates_from=token_from_rates,best_rates_to=token_to_rates)
    pprint(total_rate)
    


# best_rate = asyncio.run(
#         exchange_hub(token_from='RUB', token_to='BTC', chain_from='Кукуруза', chain_to='Bitcoin', amount=15000))
# print(best_rate)
s = time.time()
best_rate = asyncio.run(exchange_hub_double(token_from='USDT', token_to='BTC', chain_from='Tether BEP20',
                                            chain_to='Bitcoin', amount=50))
print(best_rate)
p = time.time()
print(p - s)
