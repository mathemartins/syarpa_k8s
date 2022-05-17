from django.contrib import admin

# Register your models here.
from wallet.models import (
    Ethereum, TetherUSD, BitcoinMnemonics, LedgerAccount,
    Address, BinanceCoin, BinanceUSD
)

admin.site.register(BitcoinMnemonics)
admin.site.register(LedgerAccount)
admin.site.register(Address)
admin.site.register(Ethereum)
admin.site.register(TetherUSD)
admin.site.register(BinanceCoin)
admin.site.register(BinanceUSD)
