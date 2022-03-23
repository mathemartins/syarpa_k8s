from django.db import models


# Create your models here.

class Coin(models.Model):
    name = models.CharField(max_length=200)
    coin_id = models.CharField(max_length=200, blank=True, null=True)
    symbol = models.CharField(max_length=200)
    price = models.FloatField(default=0, blank=True, null=True)
    rank = models.IntegerField(default=0, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    market_cap = models.CharField(max_length=200, blank=True, null=True)
    fully_diluted_valuation = models.CharField(max_length=200, blank=True, null=True)
    total_volume = models.CharField(max_length=200, blank=True, null=True)
    highest_in_the_last_24h = models.FloatField(default=0, blank=True, null=True)
    lowest_in_the_last_24h = models.FloatField(default=0, blank=True, null=True)
    price_change_in_the_last_24h = models.FloatField(default=0, blank=True, null=True)
    price_change_percentage_in_the_last_24h = models.FloatField(default=0, blank=True, null=True)
    market_cap_change_in_the_last_24h = models.FloatField(default=0, blank=True, null=True)
    market_cap_change_percentage_in_the_last_24h = models.FloatField(default=0, blank=True, null=True)
    circulating_supply = models.FloatField(default=0, blank=True, null=True)
    total_supply = models.FloatField(default=0, blank=True, null=True)
    max_supply = models.FloatField(default=0, blank=True, null=True)
    all_time_high = models.FloatField(default=0, blank=True, null=True)
    all_time_high_change_percentage = models.FloatField(default=0, blank=True, null=True)
    all_time_high_date = models.DateTimeField(blank=True, null=True)
    all_time_low = models.FloatField(default=0, blank=True, null=True)
    all_time_low_change_percentage = models.FloatField(default=0, blank=True, null=True)
    all_time_low_date = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    price_change_in_the_last_1hr = models.FloatField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.name)
