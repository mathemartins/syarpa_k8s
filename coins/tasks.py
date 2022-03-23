import requests
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.forms import model_to_dict

from coins.models import Coin

channel_layer = get_channel_layer()


@shared_task
def get_coins_data_from_coingecko():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1' \
          '&sparkline=false&price_change_percentage=1h%2C%2024h%2C%207d%2C%2014d%2C%2030d%2C%20200d%2C%201y '
    data = requests.get(url=url).json()
    print(data)

    coins = []

    for coin in data:
        obj, created = Coin.objects.get_or_create(symbol=coin['symbol'])
        obj.name = coin['name']
        obj.symbol = coin['symbol']

        if obj.price > coin['current_price']:
            state = 'fail'
        elif obj.price == coin['current_price']:
            state = 'same'
        elif obj.price < coin['current_price']:
            state = 'raise'

        obj.price = coin['current_price']
        obj.rank = coin['market_cap_rank']
        obj.image = coin['image']
        obj.coin_id = coin['id']
        obj.market_cap = coin['market_cap']
        obj.fully_diluted_valuation = coin['fully_diluted_valuation']
        obj.total_volume = coin['total_volume']
        obj.highest_in_the_last_24h = coin['high_24h']
        obj.lowest_in_the_last_24h = coin['low_24h']
        obj.price_change_in_the_last_24h = coin['price_change_24h']
        obj.price_change_percentage_in_the_last_24h = coin['price_change_percentage_24h']
        obj.market_cap_change_in_the_last_24h = coin['market_cap_change_24h']
        obj.market_cap_change_percentage_in_the_last_24h = coin['market_cap_change_percentage_24h']
        obj.circulating_supply = coin['circulating_supply']
        obj.total_supply = coin['total_supply']
        obj.max_supply = coin['max_supply']
        obj.all_time_high = coin['ath']
        obj.all_time_high_change_percentage = coin['ath_change_percentage']
        obj.all_time_high_date = coin['ath_date']
        obj.all_time_low = coin['atl']
        obj.all_time_low_change_percentage = coin['atl_change_percentage']
        obj.all_time_low_date = coin['atl_date']
        obj.last_updated = coin['last_updated']
        obj.price_change_percentage_in_the_last_24h = coin['price_change_percentage_1h_in_currency']
        obj.save()
        new_data = model_to_dict(obj)
        new_data.update({'state': state})

        coins.append(new_data)

    async_to_sync(channel_layer.group_send)('coins', {'type': 'send_new_data', 'text': coins})