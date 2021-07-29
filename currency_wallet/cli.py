import click

from currency_wallet.wallet import CurrencyWallet
from currency_wallet.utils import (
    DataWrangler,
    RandomCurrencies,
    first_possible_date,
    load_currencies,
)


@click.command()
@click.option('-c', '--curr', multiple=True,
              help='Select currencies and their % share, e.g. -c USD=50 -c EUR=50')
@click.option('-s', '--start', type=click.STRING, default=first_possible_date(),
              help='Start date, e.g. 2021-01-01')
@click.option('-f', '--funds', type=click.IntRange(min=1),
              default=1000, help='Amount of money to invest in PLN')
@click.option('-r', '--random', type=click.IntRange(min=1, max=35),
              help='Select random currencies')
@click.option('--csv', is_flag=True,
              help='Export to a CSV file')
def track_investments(curr, start, funds, random, csv):
    if random:
        currencies = RandomCurrencies(random).generate()
    else:
        currencies = [tuple(c.split('=')) for c in curr]

        # Validate input
        # 1. Currency
        codes = [c[0] for c in currencies]
        available_currencies = load_currencies()

        for code in codes:
            if code not in available_currencies:
                raise click.BadParameter(
                    f'{code} currency unavailable or does not exists, please select from: {available_currencies}'
                )

        # 2. Pct values add up to 100
        pct_values = [int(c[1]) for c in currencies]
        if sum(pct_values) != 100:
            raise click.BadParameter(
                f'Provided pct values: {pct_values} must add up to 100'
            )

    c = CurrencyWallet(start, currencies, funds)
    c.calculate_investment()

    dw = DataWrangler(c.wallet, c.start, c.end)
    dw.get_summary()

    # print out report
    click.clear()
    click.secho(f'INVESTMENT REPORT', bold=True, underline=True)
    click.echo(f'')
    click.echo(f'Timeframe: {c.start} >>> {c.end}')
    if dw.profit >= 0:
        click.secho(f'Well done! You have earned {dw.profit} PLN',
                    fg='bright_green', bold=True)
    else:
        click.secho(f'Unfortunately, you have lost {dw.profit} PLN',
                    fg='bright_red', bold=True)
    click.echo(f'')
    click.echo(dw.summary)
    click.echo(f'')

    # export to csv
    if csv and not dw.summary.empty:
        dw.summary.to_csv('currency-wallet-summary.csv')


def cli():
    track_investments()
