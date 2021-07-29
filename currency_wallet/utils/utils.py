import datetime
import json
import random
import requests
import numpy as np
import pandas as pd

from pkg_resources import resource_filename


class DataWrangler:
    def __init__(self, wallet, start, end):
        self.wallet = wallet
        self.start = start
        self.end = end
        self.profit = None
        self.summary = None
        self.dataviz_data = None

    def get_summary(self):
        df = pd.DataFrame(self.wallet)
        df = df[df['effectiveDate'] == self.end].copy(deep=True)
        df['final_pct_of_total'] = round(
            (df['outcome'] / sum(df['outcome'])) * 100, 2)
        df.drop(columns=['no', 'mid', 'effectiveDate'], inplace=True)
        df.set_index('currency', inplace=True)
        self.profit = round(sum(df['profit']), 2)
        self.summary = df

    def get_dataviz_data(self):
        df = pd.DataFrame(self.wallet)
        df.rename(columns={'effectiveDate': 'date'}, inplace=True)
        df = df.pivot(index='currency', columns='date', values='pct_change')
        self.dataviz_data = df


class RandomCurrencies:
    def __init__(self, num):
        self.num = num
        self._codes = set(load_currencies().keys())

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, value):
        if not 0 < value <= 35:
            raise ValueError('Number of currencies must be between 1 and 35')
        self._num = value

    def _country_codes(self):
        """Generate random country codes"""
        return random.sample(self._codes, self.num)

    def _pct_values(self):
        """Generate random pct values that add up to 100"""
        nums = np.random.random(self.num)
        nums = [round(n / sum(nums) * 100) for n in nums]
        if 0 in nums or sum(nums) != 100:
            return self._pct_values()
        return nums

    def generate(self):
        """Return currency & percent value pairs (max 35)"""
        return [(code, pct_value) for code, pct_value
                in zip(self._country_codes(), self._pct_values())]


def first_possible_date():
    date = datetime.date.today() - datetime.timedelta(days=29)
    return date.strftime('%Y-%m-%d')


def load_currencies():
    path = resource_filename('currency_wallet.utils', 'data/currencies.json')
    with open(path, 'r') as file:
        currencies = json.load(file)
    return {c['code']: c['currency'] for c in currencies[0]['rates']}


def query_nbp_api(currency, start, end):
    """Get exchange rates from NBP api"""
    adapter = requests.adapters.HTTPAdapter(max_retries=2)
    session = requests.Session()
    session.mount('http://api.nbp.pl/', adapter)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }
    url = f'http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{start}/{end}/?format=json'

    try:
        response = session.get(url, headers=headers, timeout=3)
        response.raise_for_status()
        result = response.json()
    except Exception as e:
        print(e)

    return result
