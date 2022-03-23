from rest_framework import serializers

from coins.models import Coin


class CoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coin
        fields = [
            'name',
            'coin_id',
            'symbol',
            'price',
            'rank',
            'image',
            'market_cap',
            'fully_diluted_valuation',
            'total_volume',
            'highest_in_the_last_24h',
            'lowest_in_the_last_24h',
            'price_change_in_the_last_24h',
            'price_change_percentage_in_the_last_24h',
            'market_cap_change_in_the_last_24h',
            'market_cap_change_percentage_in_the_last_24h',
            'circulating_supply',
            'total_supply',
            'max_supply',
            'all_time_high',
            'all_time_high_change_percentage',
            'all_time_high_date',
            'all_time_low',
            'all_time_low_change_percentage',
            'all_time_low_date',
            'last_updated',
            'price_change_in_the_last_1hr',
        ]