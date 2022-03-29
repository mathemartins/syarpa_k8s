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


class Bitcoin(models.Model):
    uuid = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256, default='Bitcoin')
    short_name = models.CharField(max_length=12, default='BTC')
    icon = models.URLField(blank=True, null=True)
    encrypted_private_key = models.TextField(blank=True, null=True)
    mnemonics = models.TextField(blank=True, null=True)
    xpub = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True, help_text='address')
    previous_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    available_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    frozen = models.BooleanField(default=False)
    frozen_bal = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bitcoin"
        verbose_name = "bitcoin"
        verbose_name_plural = "bitcoin"

    def __str__(self):
        return self.uuid