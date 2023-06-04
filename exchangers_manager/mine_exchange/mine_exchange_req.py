import asyncio
from pprint import pprint
from typing import Dict, List

import httpx

from exchangers_manager.xml_parser import xml_parse


async def fetch_and_parse_data() -> List[Dict]:
    xml_data = httpx.get('https://mine.exchange/request-exportxml.xml?lang=ru')
    parsed_xml_data = await xml_parse(xml_data.text)
    return parsed_xml_data


# pprint(asyncio.run(fetch_and_parse_data()))


# 'https://mine.exchange/exchange_USDTERC20_to_CPTSRUB/'