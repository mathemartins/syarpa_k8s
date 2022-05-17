from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse

from rates.models import FiatRate


class P2PTrade(models.Model):
    TRADE_TYPE = (
        ('I WANT TO BUY', 'I WANT TO BUY'),
        ('I WANT TO SELL', 'I WANT TO SELL'),
    )

    ASSET = (
        ('ETH', 'ETH'),
        ('BTC', 'BTC'),
        ('USDT', 'USDT'),
        ('DOGE', 'DOGE'),
        ('LTC', 'LTC'),
    )

    trade_creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trade_author')
    transactions = models.PositiveIntegerField(default=0)
    trade_listed_as = models.CharField(choices=TRADE_TYPE, max_length=20, default='I WANT TO SELL')
    creator_rate_in_dollar = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    crypto_trading_amount = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    min_trading_amount_in_fiat = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    max_trading_amount_in_fiat = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    asset_to_trade = models.CharField(choices=ASSET, max_length=20, default='BTC')
    price_slippage = models.DecimalField(max_digits=4, decimal_places=3, default=1.000,
                                         help_text="standard 1 dollar rate")
    min_slippage = models.DecimalField(max_digits=4, decimal_places=3, default=0.980,
                                       help_text="minimum less than 1 dollar")
    max_slippage = models.DecimalField(max_digits=4, decimal_places=3, default=1.020,
                                       help_text="maximum above 1 dollar")
    active = models.BooleanField(default=True)
    owner_cancel_trade = models.BooleanField(default=False)
    slug = models.SlugField(max_length=300, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "p2p"
        verbose_name = "P2P Trade"
        verbose_name_plural = "P2P Trades"

    def __str__(self):
        return str(self.trade_creator)

    def get_absolute_url(self):
        if self.active:
            return reverse("p2p:trades", kwargs={"slug": self.slug})


class P2PTransaction(models.Model):
    TRANSACTION_STATUS = (
        ('CREATED AND RUNNING', 'CREATED AND RUNNING'),
        ('COMPLETED', 'COMPLETED'),
        ('CANCELLED', 'CANCELLED'),
        ('ON_APPEAL', 'ON_APPEAL'),
    )

    trade = models.ForeignKey(P2PTrade, on_delete=models.CASCADE)
    transaction_key = models.CharField(max_length=300, blank=True, null=True)
    trade_visitor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trade_viewer')
    crypto_unit_transacted = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    fiat_paid = models.CharField(max_length=300, blank=True, null=True)
    status = models.CharField(choices=TRANSACTION_STATUS, max_length=20, default='CREATED AND RUNNING')
    slug = models.SlugField(max_length=300, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "p2p_transaction"
        verbose_name = "P2P Trade Transactions"
        verbose_name_plural = "P2P Trade Transactions"

    def __str__(self):
        return str(self.trade.trade_creator)

    def get_absolute_url(self):
        if self.active:
            return reverse("p2p:trades", kwargs={"slug": self.slug})


class P2PTradeCoreSettings(models.Model):
    escrow_fee = models.FloatField(default=0.8)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "p2p_settings"
        verbose_name = "P2P Trade Settings"
        verbose_name_plural = "P2P Trade Settings"

    def __str__(self):
        return str(self.escrow_fee)