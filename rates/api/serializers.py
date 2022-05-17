from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from rates.models import FiatRate


class FiatRateListSerializer(serializers.ModelSerializer):
    country = SerializerMethodField()

    class Meta:
        model = FiatRate
        fields = [
            'country',
            'dollar_rate',
            'timestamp',
            'updated',
        ]

    def get_country(self, obj):
        print(obj)
        return str(obj)