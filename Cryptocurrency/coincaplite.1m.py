#!/usr/bin/env python3

import requests

# <xbar.title>Coincap Lite</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Peter Stenger</xbar.author>
# <xbar.author.github>reteps</xbar.author.github>
# <xbar.desc>Retrieves trading information about a coin on coinmarketcap using the v2 api. </xbar.desc>
# <xbar.image>https://i.imgur.com/NiRqDUt.png</xbar.image>
# <xbar.dependencies>python3</xbar.dependencies>

coins_usd = ['bitcoin','ethereum','litecoin']

coins_btc = ['stellar','monero']

class DoesNotExistError(Exception):
    pass

def return_id(name):
    for coin in ALL_COINS:
        if coin["website_slug"] == name:
            return coin["id"]
    raise DoesNotExistError("Could not find the coin {}. Is that the full name coinmarketcap uses in it's URL?".format(name))

def display_coins(coins, display_in="USD"):
    formats = {
            "USD":"{: <5} {:0<9.3f} {:0<+6.2f}% {:0<+6.2f}% {:0>3}|href='https://coinmarketcap.com/currencies/{}' font='Menlo'",
            "BTC":"{: <5} {:0<9.7f} {:0<+6.2f}% {:0<+6.2f}% {:0>3}|href='https://coinmarketcap.com/currencies/{}' font='Menlo'"
    }
    for coin in coins:
        coin_id = return_id(coin)
        data = requests.get("https://api.coinmarketcap.com/v2/ticker/{}?convert={}".format(coin_id, display_in)).json()["data"]
        print(formats[display_in].format(data["symbol"], data["quotes"][display_in]["price"], data["quotes"][display_in]["percent_change_24h"], \
                data["quotes"][display_in]["percent_change_7d"], data["rank"], data["website_slug"]))


print('Ƀ')
print('---')
ALL_COINS = requests.get("https://api.coinmarketcap.com/v2/listings").json()["data"]
IMAGE_URL = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/{}.png"
print('COIN     USD    24 HOUR  7 DAY  RANK|font="Menlo"')
display_coins(coins_usd)
print('COIN     BTC    24 HOUR  7 DAY  RANK|font="Menlo"')
display_coins(coins_btc, display_in="BTC")
