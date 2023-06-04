import asyncio
from pprint import pprint
from typing import Dict
from exchangers_manager.alfabit import alfabit_req
from exchangers_manager.scsobmen import scsobmen_req
# from exchangers_manager.e365cash import e365cash_req
from exchangers_manager.expochange import expochange_req
from exchangers_manager.mine_exchange import mine_exchange_req
from exchangers_manager.royal import royal_req


class BestExchange:
    
    def __init__(self) -> None:
        self.alfabit_chain = None
        self.scsobmen_chain = None
        # self.e365cash_chain = None
        self.expochange_chain = None
        self.mine_exchange_chain = None
    
    async def create(self):
        self.alfabit_chain, self.scsobmen_chain, self.expochange_chain, self.mine_exchange_chain = await asyncio.gather(
                alfabit_req.fetch_and_parse_data(),
                scsobmen_req.fetch_and_parse_data(),
                expochange_req.fetch_and_parse_data(),
                mine_exchange_req.fetch_and_parse_data()
        )
        return
    
    async def best_single(self, from_currency, to_currency) -> Dict:
        # pprint(list(exchange for exchange in self.alfabit_chain))
        # pprint(list(exchange for exchange in self.scsobmen_chain))
        # pprint(list(exchange for exchange in self.expochange_chain))
        # pprint(list(exchange for exchange in self.mine_exchange_chain))
        all_chains = {'alfabit_chain': [exchange for exchange in self.alfabit_chain if
                                        from_currency in exchange['from_currency'] and
                                        to_currency in exchange['to_currency']],
                      'scsobmen_chain': [exchange for exchange in self.scsobmen_chain if
                                         from_currency in exchange['from_currency'] and
                                         to_currency in exchange['to_currency']],
                      'expochange_chain': [exchange for exchange in self.expochange_chain if
                                           from_currency in exchange['from_currency'] and
                                           to_currency in exchange['to_currency']],
                      'mine_exchange_chain': [exchange for exchange in self.mine_exchange_chain if
                                              from_currency in exchange['from_currency'] and
                                              to_currency in exchange['to_currency']]}
        # 'royal_chain': await royal_req.track_a_couple(from_currency.lower(), to_currency.lower())
        best_exchange = None
        best_exchanger = None
        best_rate = 0
        
        for exchanger, exchanges in all_chains.items():
            for exchange in exchanges:
                rate = float(exchange['exchange_rate'])
                if rate > best_rate:
                    best_rate = rate
                    best_exchange = exchange
                    best_exchanger = exchanger
        
        print(f"The best exchange rate is {best_rate} at {best_exchanger}.")
        print(f"The details of the exchange are: {best_exchange}")

        return best_exchange
    
    async def best_double(self, from_currency, to_currency) -> Dict:
        ...
    
    async def best_triple(self, from_currency, to_currency) -> Dict:
        ...


best = BestExchange()
asyncio.run(best.create())
# print(best.expochange_chain)
# print(best.alfabit_chain)
pprint(asyncio.run(best.best_single('RUB', 'USDTTRC20')))
