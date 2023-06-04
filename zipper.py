import requests
import zipfile
import io
import codecs
from operator import itemgetter

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

# Sort and print the rates
from_cy = '93'  # Bitcoin
to_cy = '139'  # Ethereum

print(f"Exchange rates in the direction {currencies[from_cy]} -> {currencies[to_cy]}:")
sorted_rates = sorted(rates[from_cy][to_cy].items(), key=lambda x: x[1]['rate'])
for exch_id, entry in sorted_rates:
    print(f"{exchangers[exch_id]} - reviews {entry['reviews']} - rate {entry['rate']} {currencies[from_cy]} -> {currencies[to_cy]} - reserve {entry['reserve']} {currencies[to_cy]}")

# Print the currency list
print("\nCurrency list:")
for cy_id, cy_name in sorted(currencies.items()):
    print(f"{cy_id} - {cy_name}")

# Print the exchanger list
print("\nExchanger list:")
for exch_id, exch_name in sorted(exchangers.items()):
    print(f"{exch_id} - {exch_name}")
