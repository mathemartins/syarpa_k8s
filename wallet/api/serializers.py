from rest_framework import serializers

from wallet.models import Ethereum


class EthereumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ethereum
        fields = [
            'uuid',
            'name',
            'short_name',
            'icon',
            'encrypted_private_key',
            'public_key',
            'previous_bal',
            'available_bal',
            'frozen_bal',
            'timestamp',
            'updated',
        ]