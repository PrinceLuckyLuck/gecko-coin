from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
bitcoin_price = cg.get_coin_ticker_by_id('bitcoin', exchange_ids='binance')['tickers'][0]['last']
print(bitcoin_price)