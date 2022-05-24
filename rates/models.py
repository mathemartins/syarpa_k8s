
from django.db import models

# Create your models here.
from django_countries.fields import CountryField


# class FiatRate(models.Model):
#     country = CountryField(blank=True, null=True, max_length=255)
#     dollar_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = "fiat_rate"
#         verbose_name = "Fiat Rate"
#         verbose_name_plural = "Fiat Rates"
#
#     def __str__(self):
#         return str(self.country.name)