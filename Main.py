from binance.client import Client
import time, os
from playsound import playsound

# <!> Buy COIN manually right before executing the code <!>

# Define your API key and secret
API_KEY = os.getenv("MY_KEY")
API_SECRET = os.getenv("MY_API_SECRET")

# Define the client
client = Client(API_KEY, API_SECRET)

# Trading between:
coin = 'BTC'
pairing = 'BUSD'

is_coin_owned = True
min_coin_value = float(client.get_symbol_ticker(symbol=coin + pairing)['price'])
max_coin_value = float(client.get_symbol_ticker(symbol=coin + pairing)['price'])
print(f">>>> BUYING PRICE: {min_coin_value}$ <<<<")
percentage_sell_coin = 0.0015
percentage_buy_coin = 0.003

while True:
    try:
        coin_value = float(client.get_symbol_ticker(symbol=coin + pairing)['price'])
        if coin_value > max_coin_value:
            max_coin_value = coin_value
        if coin_value < (1 - percentage_sell_coin) * max_coin_value and is_coin_owned:
            print(f">>>> SELLING {coin} <<<<")
            quantity = float(client.get_asset_balance(asset=coin)['free'])
            client.order_market_sell(symbol=coin + pairing, quantity=quantity)
            pairing_owned = float(client.get_asset_balance(asset=pairing)['free'])
            print(f">>>> SELLING PRICE: {coin_value}$ <<<<")
            print(f">>>> YOU NOW HAVE: {pairing_owned}$ <<<<")
            is_coin_owned = False
            min_coin_value = coin_value
        if coin_value < min_coin_value:
            min_coin_value = coin_value
        if coin_value > (1 + percentage_buy_coin) * min_coin_value and not is_coin_owned:
            print(f">>>> BUYING {coin} <<<<")
            quote_order_qty = float(client.get_asset_balance(asset=pairing)['free'])
            client.order_market_buy(symbol=coin + pairing, quoteOrderQty=quote_order_qty)
            print(f">>>> BUYING PRICE: {coin_value}$ <<<<")
            is_coin_owned = True
            max_coin_value = coin_value
    except Exception as e:
        print(f"Error: {e}")
        playsound('warning.mp3')
    time.sleep(3)
