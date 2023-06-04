from typing import Dict, List


import xml.etree.ElementTree as ET




async def xml_parse(xml_data: str) -> List[Dict]:
    # Parse the XML data
    root = ET.fromstring(xml_data)
    # Extract information from each 'item' element
    items = root.findall('item')
    parsed_xml_data = []
    for item in items:
        from_currency = item.find('from').text

        to_currency = item.find('to').text
        in_value = float(item.find('in').text)
        out_value = float(item.find('out').text)
        amount = float(item.find('amount').text)
        min_exchange_amount = float(item.find('minamount').text.split(' ')[0])
        exchange_rate = "{:.8f}".format(out_value / in_value)
        parsed_xml_data.append({'from_currency': from_currency,
                                'to_currency': to_currency,
                                'exchange_rate': exchange_rate,
                                'reserve': amount,
                                'min_exchange_amount': min_exchange_amount})
    return parsed_xml_data
