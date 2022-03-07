import json
import os

from rest_framework import serializers

from wallet.api.utils import EtherChain
from wallet.models import Ethereum

chain_connection = EtherChain(infura_endpoint=os.environ.get('INFURA_ENDPOINT'))


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

    def create(self, validated_data: dict):
        print(validated_data, type(validated_data))
        wallet = chain_connection.create_wallet()
        print(wallet.address)
        wallet_obj = Ethereum(
            uuid=validated_data.get('uuid', ),
            icon="https://cryptologos.cc/logos/ethereum-eth-logo.png",
            encrypted_private_key=str(json.dumps(wallet.encrypt(validated_data.get('uuid', ))),),
            public_key=str(wallet.address),
        )
        wallet_obj.save()
        return wallet_obj
