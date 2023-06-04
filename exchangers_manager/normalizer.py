from manifests.tokens_manifest import Tokens


def normalize(value):
    bank_currency = value.split(' ')
    currency = bank_currency.pop(-1)
    bank_currency = list(map(lambda x: x.replace('-', ''), bank_currency))
    bank_currency = '-'.join(bank_currency)
    if bank_currency.lower() in Tokens.bank_abbreviations:
        bank = Tokens.bank_abbreviations[bank_currency.lower()]
        return bank + currency if bank_currency != currency else bank
    elif bank_currency in Tokens.token_chains:
        bank = Tokens.token_chains[bank_currency.lower()]
        return bank
    else:
        return None, None
