from django.contrib import admin

# Register your models here.
from wallet.models import Ethereum, TetherUSD

admin.site.register(Ethereum)
admin.site.register(TetherUSD)