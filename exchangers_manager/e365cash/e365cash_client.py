import asyncio
from pprint import pprint
from typing import List, Dict

from playwright.async_api import async_playwright

from manifests.exchangers_manifest import Exchangers
from manifests.tokens_manifest import Tokens



# это не то!
async def track_a_couple(coin_from: str, coin_to: str) -> List[Dict]:
    """
    function from parsing coin couples bestchange.ru
    :param coin_from:
    :param coin_to:
    :return List[Dict]:
    """
    # Connect to playwright sesscion
    async with async_playwright() as p:
        browser_type = p.firefox
        browser = await browser_type.launch(headless=True, timeout=50000)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f'https://www.bestchange.ru/{coin_from}-to-{coin_to}.html')
        
        # Take element
        ca = await page.query_selector_all('[class="ca"]')  # exchange name
        fs = await page.query_selector_all('[class="fs"]')  # give amount in coin_from
        bi = await page.query_selector_all('[class="bi"]')  # min limit
        fm = await page.query_selector_all('[class="fm"]')  # get amount in coin_to
        reserve = await page.query_selector_all('[class="ar arp"]')  # coin reserve
        rate = await page.query_selector_all('[class="rw"]')  # reviews count
        
        # Extract the text content from each element
        ca_texts = [await item.inner_text() for item in ca]
        fs_texts = [await item.inner_text() for item in fs]
        bi_texts = [await bi[item].inner_text() for item in range(1, len(bi), 2)]
        fm_texts = [await item.inner_text() for item in fm]
        reserve_texts = [await item.inner_text() for item in reserve]
        rate_texts = [await item.inner_text() for item in rate]
        grouped_data = []
        
        # formatter
        for index, values in enumerate(zip(ca_texts, fs_texts, bi_texts, fm_texts, reserve_texts, rate_texts)):
            if values[0] in Exchangers.exchangers_valid_name:  # Append only needed exchangers
                group_dict = {
                    'exchange_name': values[0],
                    'give': values[1],
                    'get': values[2],
                    'min_limit': values[3],
                    'reserve': values[4],
                    'rate': values[5]
                }
                grouped_data.append(group_dict)
        pprint(grouped_data)
        return grouped_data


# PC DESTROYER
async def gather_track_a_couple():
    tasks = [track_a_couple(coin_from=Tokens.tokens_valid[i],
                            coin_to=Tokens.tokens_valid[i + 1]) for i in range(len(Tokens.tokens_valid[:-1]))]
    fetched_data = await asyncio.gather(*tasks)
    combined_data = [item for sublist in fetched_data for item in sublist]
    return combined_data


# PC DESTROYER 2.0
async def gather_with_concurrency(n, *coros):
    semaphore = asyncio.Semaphore(n)
    tasks = [track_a_couple(coin_from=Tokens.tokens_valid[i],
                            coin_to=Tokens.tokens_valid[i + 1]) for i in range(len(Tokens.tokens_valid[:-1]))]
    await gather_with_concurrency(5, *tasks)
    
    async def sem_coro(coro):
        async with semaphore:
            return await coro
    
    return await asyncio.gather(*(sem_coro(c) for c in coros))


async def find_best_exchange(coin_from: str, coin_to: str) -> Dict:
    print('\ncouple:', coin_from, coin_to)
    exchangers_info_list = await track_a_couple(coin_from=coin_from, coin_to=coin_to)
    max_give = max(exchangers_info_list, key=lambda x: float(x['give'].split()[0]))
    print('Exchange name:', max_give['exchange_name'])
    print('Maximum give:', max_give['give'])
    
    return max_give


if __name__ == '__main__':
    for i in range(len(Tokens.tokens_valid[:-1])):
        print('\ncouple:', Tokens.tokens_valid[i], Tokens.tokens_valid[i + 1])
        asyncio.run(track_a_couple(coin_from=Tokens.tokens_valid[i], coin_to=Tokens.tokens_valid[i + 1]))

