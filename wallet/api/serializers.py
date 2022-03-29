import json
import os

from rest_framework import serializers

from wallet.api.utils import EtherChain, OminiChain
from wallet.models import Ethereum, TetherUSD, Bitcoin

chain_connection = EtherChain(infura_endpoint=os.environ.get('INFURA_ENDPOINT'))
omini_connection = OminiChain(
    tatum_endpoint=os.environ.get('TATUM_API'),
    network_type=os.environ.get('TATUM_NETWORK_TYPE'),
    base_url=os.environ.get('TATUM_BASE_URL'),
)


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
            encrypted_private_key=str(json.dumps(wallet.encrypt(validated_data.get('uuid', ))), ),
            public_key=str(wallet.address),
        )
        wallet_obj.save()
        return wallet_obj


class USDTSerializer(serializers.ModelSerializer):
    class Meta:
        model = TetherUSD
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
        try:
            user_eth_wallet = Ethereum.objects.get(uuid=validated_data.get('uuid'))
            wallet_obj = TetherUSD(
                uuid=validated_data.get('uuid', ),
                icon="https://cryptologos.cc/logos/tether-usdt-logo.png",
                encrypted_private_key=user_eth_wallet.encrypted_private_key,
                public_key=user_eth_wallet.public_key,
            )
            wallet_obj.save()
            return wallet_obj
        except user_eth_wallet.DoesNotExist:
            raise serializers.ValidationError("User must have an ethereum wallet first!")


class BitcoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bitcoin
        fields = [
            'uuid',
            'name',
            'short_name',
            'icon',
            'encrypted_private_key',
            'xpub',
            'mnemonic',
            'public_key',
            'previous_bal',
            'available_bal',
            'frozen_bal',
            'timestamp',
            'updated',
        ]

    def create(self, validated_data: dict):
        print(validated_data, type(validated_data))
        wallet: dict = omini_connection.create_wallet()
        wallet_obj = Bitcoin(
            uuid=validated_data.get('uuid', ),
            icon="https://cryptologos.cc/logos/bitcoin-btc-logo.png",
            xpub=wallet.get('xpub'),
            mnemonics=wallet.get('mnemonic'),
            encrypted_private_key=wallet.get('private_key'),
            public_key=wallet.get('address'),
        )
        wallet_obj.save()
        return wallet_obj
