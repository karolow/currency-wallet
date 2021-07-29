from datetime import (
    date,
    datetime,
    timedelta,
)
from currency_wallet.utils import (
    first_possible_date,
    query_nbp_api,
)


class CurrencyWallet:
    def __init__(self, start, currencies, funds):
        self.start = start
        self.currencies = currencies
        self.funds = funds
        self.end = None
        self.valid_start_rate = self._get_closest_weekday()
        self.wallet = None
        self._get_end_date()

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if not isinstance(value, date):
            value = datetime.strptime(value, "%Y-%m-%d").date()
        if value + timedelta(days=29) > date.today():
            raise ValueError(
                f"Start date must be {first_possible_date().strftime('%Y-%m-%d')} or earlier")
        self._start = value

    def calculate_investment(self):

        output = []

        for val in self.currencies:

            currency, pct = val
            pct = int(pct)
            api_response = query_nbp_api(
                currency, self.valid_start_rate, self.end)
            investment_pln, investment = self._get_initial_params(pct, api_response)

            for num, row in enumerate(api_response.get('rates'), 1):
                row['currency'] = currency
                if num == 1:
                    row['effectiveDate'] = self.start.strftime('%Y-%m-%d')
                row['pct_of_total'] = pct
                row['investment'] = investment_pln
                value_in_pln = investment * row['mid']
                row['outcome'] = round(value_in_pln, 3)
                row['pct_change'] = round((value_in_pln / investment_pln) - 1, 3)
                row['profit'] = round(value_in_pln - investment_pln, 3)
                output.append(row)

        self.wallet = output
        # if data for current day unavailable,
        # use the last available as the end date
        last_row = output[-1]
        self.end = last_row['effectiveDate']

    def _get_initial_params(self, pct, api_response):
        investment_pln = self.funds * pct * 0.01
        exch_rate = api_response['rates'][0]['mid']
        investment = investment_pln / exch_rate
        return investment_pln, investment

    def _get_closest_weekday(self):
        if self.start.isoweekday() in [6, 7]:
            date = self.start - timedelta(days=self.start.isoweekday() - 5)
            return date.strftime('%Y-%m-%d')
        return self.start.strftime('%Y-%m-%d')

    def _get_end_date(self):
        end = self.start + timedelta(days=29)
        self.end = end.strftime("%Y-%m-%d")
