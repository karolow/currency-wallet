from setuptools import setup, find_packages

setup(
    name='currency-wallet',
    version='0.1.0',
    description="Track investment returns in multiple currencies through the National Bank of Poland's API.",
    packages=find_packages(include=['currency_wallet']),
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['currency-wallet=currency_wallet.cli:cli'],
    },
)
