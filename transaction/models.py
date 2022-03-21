from django.db import models


# Create your models here.

class Transaction(models.Model):
    TransactionType = (
        ('off-chain', 'off-chain'),
        ('on-chain', 'on-chain')
    )
    sender = models.CharField(max_length=200)
    receiver = models.CharField(max_length=200)
    amount = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    balance_after_transaction = models.DecimalField(decimal_places=18, default=0, max_digits=100)
    transacting_currency = models.CharField(max_length=200)
    transaction_type = models.CharField(choices=TransactionType, max_length=200)
    hash = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sender
