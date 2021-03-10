from pycoingecko import CoinGeckoAPI
import time

cg = CoinGeckoAPI()

coins = cg.get_coins_list()
coins_id = []
for coin in coins:
    coins_id.append(coin['id'])

def clear_coins(ids, param):


    clear_coins_id = []
    i = 0
    for id in ids:
        if param in id:
            print(f'deleted: {id}')
            i += 1
        else:
            clear_coins_id.append(id)
    print(i)
    return clear_coins_id

# g = clear_coins(coins_id, '-long')
# print(g)
# print(len(g))
# sec = clear_coins(g, '-short')
# print(sec)
# print(len(sec))
# third = clear_coins(sec, '-set')
# print(third)
# print(len(third))


def exchange_coins(pages, exchange, coin):
    coins = []
    for page in range(1, pages + 1):
        tickers = cg.get_exchanges_tickers_by_id(exchange, page=page)
        for ticker in tickers['tickers']:
            if ticker['target'] == coin:
                coins.append(ticker['coin_id'])
        time.sleep(0.6)
    return coins
binance_coins = exchange_coins(10, 'binance', 'BTC')
gate_coins = exchange_coins(12, 'gate', 'USDT')
print(binance_coins, len(binance_coins), gate_coins, len(gate_coins), sep='\n')
exchanges_coins = list(set(binance_coins) & set(gate_coins))
print(exchanges_coins, len(exchanges_coins), sep='\n')

bitcoin_binance_price_in_usdt = cg.get_coin_ticker_by_id('bitcoin', exchange_ids='binance')['tickers'][0]['last']
print(bitcoin_binance_price_in_usdt)

def coins_price(pages, exchange, coins, t):
    info = []
    for page in range(1, pages + 1):
        tickers = cg.get_exchanges_tickers_by_id(exchange, page=page)
        for ticker in tickers['tickers']:
            if ticker['target'] == t and ticker['last'] > 0 and ticker['coin_id'] in coins:
                coin = {}
                coin['name'] = ticker['base']
                coin['id'] = ticker['coin_id']
                coin['price'] = ticker['last']
                info.append(coin)
        time.sleep(0.6)
    return info
binance_coins_price = coins_price(10, 'binance', exchanges_coins, 'BTC')
gate_coins_price = coins_price(12, 'gate', exchanges_coins, 'USDT')
print(binance_coins_price, len(binance_coins_price), gate_coins_price, len(gate_coins_price), sep='\n')

for i in binance_coins_price:
    for j in gate_coins_price:
        if i['name'] == j['name']:
            price_in_usdt = i['price'] * bitcoin_binance_price_in_usdt
            i['usdt'] = price_in_usdt
            difference = abs(price_in_usdt / j['price'] - 1) * 100
            if difference > 3:
                print(i, j, f'{round(difference, 2)}%')