import asyncio
from typing import Dict, List

import httpx

from exchangers_manager.xml_parser import xml_parse

# STATUS CODE = 502
async def check_exchange_rates() -> List[Dict]:
    xml_data = httpx.get('https://kassa.cc/api/v1/rate_calculations')
    print(xml_data.text)
    xml_data = xml_data.text
    parsed_xml_data = await xml_parse(xml_data)
    
    return parsed_xml_data

asyncio.run(check_exchange_rates())
