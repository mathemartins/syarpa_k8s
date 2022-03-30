from django.contrib import admin

# Register your models here.
from wallet.models import Ethereum, TetherUSD, Bitcoin, BinanceCoin, BinanceUSD

admin.site.register(Bitcoin)
admin.site.register(Ethereum)
admin.site.register(TetherUSD)
admin.site.register(BinanceCoin)
admin.site.register(BinanceUSD)
