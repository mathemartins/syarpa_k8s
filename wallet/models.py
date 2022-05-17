from django.db import models


# Create your models here.

class Ethereum(models.Model):
    uuid = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256, default='Ethereum')
    short_name = models.CharField(max_length=12, default='ETH')
    icon = models.URLField(blank=True, null=True)
    encrypted_private_key = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True, help_text='address')
    previous_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    available_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    frozen = models.BooleanField(default=False)
    frozen_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ethereum"
        verbose_name = "Ethereum"
        verbose_name_plural = "Ethereum"

    def __str__(self):
        return self.uuid


class TetherUSD(models.Model):
    uuid = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256, default='TetherUSD')
    short_name = models.CharField(max_length=12, default='USDT')
    network = models.CharField(max_length=256, default="ERC20")
    icon = models.URLField(blank=True, null=True)
    encrypted_private_key = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True, help_text='address')
    previous_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    available_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    frozen = models.BooleanField(default=False)
    frozen_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tetherUsd"
        verbose_name = "tetherUsd"
        verbose_name_plural = "tetherUsd"

    def __str__(self):
        return self.uuid


class BinanceCoin(models.Model):
    uuid = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256, default='BinanceCoin')
    short_name = models.CharField(max_length=12, default='BNB')
    icon = models.URLField(blank=True, null=True)
    encrypted_private_key = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True, help_text='address')
    previous_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    available_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    frozen = models.BooleanField(default=False)
    frozen_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "binancecoin"
        verbose_name = "binancecoin"
        verbose_name_plural = "binancecoin"

    def __str__(self):
        return self.uuid


class BinanceUSD(models.Model):
    uuid = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256, default='BinanceUSD')
    short_name = models.CharField(max_length=12, default='BUSD')
    icon = models.URLField(blank=True, null=True)
    encrypted_private_key = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True, help_text='address')
    previous_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    available_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    frozen = models.BooleanField(default=False)
    frozen_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "binanceusd"
        verbose_name = "binanceusd"
        verbose_name_plural = "binanceusd"

    def __str__(self):
        return self.uuid


class TetherUSDBEP20(models.Model):
    uuid = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256, default='TetherUSD')
    short_name = models.CharField(max_length=12, default='USDT')
    network = models.CharField(max_length=256, default="BEP20")
    icon = models.URLField(blank=True, null=True)
    encrypted_private_key = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True, help_text='address')
    previous_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    available_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    frozen = models.BooleanField(default=False)
    frozen_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tetherUsdBEP20"
        verbose_name = "tetherUsdBEP20"
        verbose_name_plural = "tetherUsdBEP20"

    def __str__(self):
        return self.uuid


class Tron(models.Model):
    uuid = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256, default='Tron')
    short_name = models.CharField(max_length=12, default='TRX')
    icon = models.URLField(blank=True, null=True)
    encrypted_private_key = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True, help_text='address')
    previous_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    available_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    frozen = models.BooleanField(default=False)
    frozen_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tron"
        verbose_name = "tron"
        verbose_name_plural = "tron"

    def __str__(self):
        return self.uuid


class TetherUSDTRC20(models.Model):
    uuid = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256, default='TetherUSD')
    short_name = models.CharField(max_length=12, default='USDT')
    network = models.CharField(max_length=256, default="BEP20")
    icon = models.URLField(blank=True, null=True)
    encrypted_private_key = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True, help_text='address')
    previous_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    available_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    frozen = models.BooleanField(default=False)
    frozen_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tetherUsdTRC20"
        verbose_name = "tetherUsdTRC20"
        verbose_name_plural = "tetherUsdTRC20"

    def __str__(self):
        return self.uuid


# Create your models here.
class BitcoinMnemonics(models.Model):
    uuid = models.CharField(max_length=500, blank=True, null=True)
    seed_phrase = models.TextField()
    xpub = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bitcoin_mnemonics"
        verbose_name = "bitcoin mnemonics"
        verbose_name_plural = "bitcoin mnemonics"

    def __str__(self):
        return self.xpub


class LedgerAccount(models.Model):
    coin_symbol = models.CharField(max_length=300)
    active = models.BooleanField(default=True)
    available_balance = models.CharField(max_length=300)
    account_balance = models.CharField(max_length=300)
    frozen = models.BooleanField(default=False)
    xpub = models.ForeignKey(BitcoinMnemonics, on_delete=models.CASCADE, blank=True, null=True)
    customer_id = models.CharField(max_length=300)
    currency = models.CharField(max_length=300, default="USD")
    ledger_id = models.CharField(max_length=300)

    class Meta:
        db_table = "ledger_account"
        verbose_name = "ledger account"
        verbose_name_plural = "ledger accounts"

    def __str__(self):
        return self.ledger_id


class Address(models.Model):
    xpub = models.ForeignKey(BitcoinMnemonics, on_delete=models.CASCADE, blank=True, null=True)
    derivation_key = models.IntegerField()
    address_key = models.CharField(max_length=300)
    coin_symbol = models.CharField(max_length=300)

    class Meta:
        db_table = "address"
        verbose_name = "address"
        verbose_name_plural = "address"

    def __str__(self):
        return self.address_key