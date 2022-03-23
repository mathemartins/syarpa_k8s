from django.contrib import admin

# Register your models here.
from coins.models import Coin


class CoinModelAdmin(admin.ModelAdmin):
    list_display = ('rank', 'name', 'symbol', 'price', 'market_cap', 'highest_in_the_last_24h', 'lowest_in_the_last_24h')
    list_display_links = ('name', 'price',)
    search_fields = ('name', 'symbol',)


admin.site.register(Coin, CoinModelAdmin)