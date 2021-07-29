# currency-wallet

Track investment returns in currencies through the National Bank of Poland's API.

The tool monitors investment returns in up to 35 basic currencies, the exchange rates of which are published by the National Bank of Poland in Table A (http://api.nbp.pl/).

Installation instructions to be found [below](https://github.com/karolow/currency-wallet).

### features & usage

* select currencies and their % share: -c EUR=30 -c USD=40 -c CZK=30
* set the start date: -s 2021-07-01
* define the amount that you want to invest (in PLN): -f 1000
* or play with --random option with up to 35 available currencies: -r 9
* see the results in your terminal or download a CSV file by adding a --csv flag

#### Example queries:

```shell
currency-wallet --random 3
```

This command will randomly select 3 currencies and generate a report for default values: a 1000PLN investment over the past 30 days.

![random_3_currencies](https://karolpiekar.ski/images/screens/currency-wallet/currency-wallet_random_3.png)

```shell
currency-wallet -c ISK=17 -c NOK=56 -c HUF=27 -s 2021-04-21 -f 1000 --csv
```

![selected_3_currencies](https://karolpiekar.ski/images/screens/currency-wallet/currency-wallet_selected_3.png)

This one will check the exchange rates between 2021-04-21 and 2021-05-20 for 3 selected currencies (ISK: 17%, NOK: 56%, HUF: 27%) that were bought for 1000PLN. The results will be exported to a CSV file. 

#### CLI documentation:

```shell
Usage: currency-wallet [OPTIONS]

Options:
  -c, --curr TEXT             Select currencies and their % share, e.g. -c
                              USD=50 -c EUR=50
  -s, --start TEXT            Start date, e.g. 2021-01-01
  -f, --funds INTEGER RANGE   Amount of money to invest in PLN  [x>=1]
  -r, --random INTEGER RANGE  Select random currencies  [1<=x<=35]
  --csv                       Export to a CSV file
  --help                      Show this message and exit.
```

### installation

```shell
git clone https://github.com/karolow/currency-wallet.git
cd currency-wallet

pip install -e . -r requirements.txt
```

### available currencies

```
'THB': 'bat (Tajlandia)'
'USD': 'dolar amerykański'
'AUD': 'dolar australijski'
'HKD': 'dolar Hongkongu'
'CAD': 'dolar kanadyjski'
'NZD': 'dolar nowozelandzki'
'SGD': 'dolar singapurski'
'EUR': 'euro'
'HUF': 'forint (Węgry)'
'CHF': 'frank szwajcarski'
'GBP': 'funt szterling'
'UAH': 'hrywna (Ukraina)'
'JPY': 'jen (Japonia)'
'CZK': 'korona czeska'
'DKK': 'korona duńska'
'ISK': 'korona islandzka'
'NOK': 'korona norweska'
'SEK': 'korona szwedzka'
'HRK': 'kuna (Chorwacja)'
'RON': 'lej rumuński'
'BGN': 'lew (Bułgaria)'
'TRY': 'lira turecka'
'ILS': 'nowy izraelski szekel'
'CLP': 'peso chilijskie'
'PHP': 'peso filipińskie'
'MXN': 'peso meksykańskie'
'ZAR': 'rand (Republika Południowej Afryki)'
'BRL': 'real (Brazylia)'
'MYR': 'ringgit (Malezja)'
'RUB': 'rubel rosyjski'
'IDR': 'rupia indonezyjska'
'INR': 'rupia indyjska'
'KRW': 'won południowokoreański'
'CNY': 'yuan renminbi (Chiny)'
'XDR': 'SDR (MFW)'
```
