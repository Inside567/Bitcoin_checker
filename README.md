# Bitcoin_checker
Script for using the BlockIO API to check the transactions of a specified wallet

Prior to running bitcoin_checker.py you will likely need to Pip install the BlockIO API module, which is called "block_io".

When first running this bitcoin_checker.py it will create three files in your working directory: api_keys.csv, bitcoin.csv, and config.csv. It will check if these files exist when it runs, and won't re-create or overwrite them if they already exist.

The api_keys.csv is to store the API key and secret pin you get from your BlockIO account. The API key should be in A1, and the secret pin in A2.

The bitcoin.csv file will store results from each time bitcoin_checker.py is ran. It will also check for previous results, and only add new items.

The config.csv is what holds the list of bitcoin wallet IDs you would like to search against. These should be added to the A column, staring in A2.

There is some very basic rate limiting in bitcoin_checker.py, but I am not sure of the rate limit on the BlockIO API. It's been working fine in testing whilst checking 20 wallets.
