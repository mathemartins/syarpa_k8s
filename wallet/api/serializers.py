import json
import os

from rest_framework import serializers

from wallet.api.utils import EtherChain, OminiChain, BinanceSmartChain
from wallet.models import Ethereum, TetherUSD, BitcoinMnemonics, BinanceCoin, TetherUSDBEP20

chain_connection = EtherChain(infura_endpoint=os.environ.get('INFURA_ENDPOINT'))
bsc_chain_connection = BinanceSmartChain(bsc_endpoint=os.environ.get('BINANCE_SMARTCHAIN'))
omini_connection = OminiChain(
    tatum_api_key=os.environ.get('TATUM_API'),
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


class BinanceCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinanceCoin
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
        wallet = bsc_chain_connection.create_wallet()
        print(wallet.address)
        wallet_obj = BinanceCoin(
            uuid=validated_data.get('uuid', ),
            icon="https://cryptologos.cc/logos/binance-bnb-logo.png",
            encrypted_private_key=str(json.dumps(wallet.encrypt(validated_data.get('uuid', ))), ),
            public_key=str(wallet.address),
        )
        wallet_obj.save()
        return wallet_obj


class USDTBinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TetherUSDBEP20
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
            user_bnb_wallet = TetherUSDBEP20.objects.get(uuid=validated_data.get('uuid'))
            wallet_obj = TetherUSDBEP20(
                uuid=validated_data.get('uuid', ),
                icon="https://cryptologos.cc/logos/tether-usdt-logo.png",
                encrypted_private_key=user_bnb_wallet.encrypted_private_key,
                public_key=user_bnb_wallet.public_key,
            )
            wallet_obj.save()
            return wallet_obj
        except user_bnb_wallet.DoesNotExist:
            raise serializers.ValidationError("User must have an binance wallet first!")


class BitcoinMnemonicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitcoinMnemonics
        fields = [
            'seed_phrase',
            'xpub',
            'timestamp',
            'updated',
        ]