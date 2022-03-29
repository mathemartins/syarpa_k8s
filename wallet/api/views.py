import hashlib
import os
import time

from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from syarpa_k8s.restconf.permissions import AnonPermissionOnly
from transaction.models import Transaction
from wallet.api.serializers import EthereumSerializer, USDTSerializer, BitcoinSerializer
from wallet.api.utils import EtherChain
from wallet.models import Ethereum, TetherUSD, Bitcoin

chain_connection = EtherChain(infura_endpoint=os.environ.get('INFURA_ENDPOINT'))


class EthereumCreate(CreateAPIView):
    permission_classes = [AnonPermissionOnly]
    queryset = Ethereum.objects.all()
    serializer_class = EthereumSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class EthereumTransfer(APIView):
    permission_classes = [AnonPermissionOnly]

    def post(self, *args, **kwargs):
        data = self.request.data
        try:
            Ethereum.objects.get(public_key=data.get('recipient'))
            print("off-chain")

            # validation before transaction
            # perform off-chain transaction and hash the timestamp
            sender_obj = Ethereum.objects.get(uuid=data.get('uuid'))
            if sender_obj.available_bal <= float(data.get('amount')):
                return Response(
                    {'message': "transaction failed due to insufficient balance"},
                    status=status.HTTP_402_PAYMENT_REQUIRED
                )
            sender_obj.previous_bal = float(sender_obj.previous_bal) - float(data.get('amount'))
            sender_obj.available_bal = float(sender_obj.available_bal) - float(data.get('amount'))
            sender_obj.save()

            recipient_obj = Ethereum.objects.get(public_key=data.get('recipient'))
            recipient_obj.previous_bal = float(recipient_obj.previous_bal) + float(data.get('amount'))
            recipient_obj.available_bal = float(recipient_obj.available_bal) + float(data.get('amount'))
            recipient_obj.save()

            tx_hash = hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest()[:60]

            # record transaction
            Transaction.objects.create(
                sender=sender_obj.public_key,
                receiver=recipient_obj.public_key,
                amount=float(data.get('amount')),
                balance_after_transaction=sender_obj.available_bal,
                transacting_currency="ETH",
                transaction_type="off-chain",
                hash=f"0x{str(tx_hash)}".upper()
            )

            return Response(
                {
                    'message': "transaction successful",
                    "tx_": f"0x{str(tx_hash)}".upper(),
                    "success": bool(tx_hash)
                },
                status=status.HTTP_201_CREATED
            )
        except Ethereum.DoesNotExist:
            print("on-chain")
            sender_obj = Ethereum.objects.get(uuid=data.get('uuid'))
            if sender_obj.available_bal <= float(data.get('amount')):
                return Response(
                    {'message': "transaction failed due to insufficient balance"},
                    status=status.HTTP_402_PAYMENT_REQUIRED
                )
            # Does not exist/not a syarpa user perform on-chain transaction
            amount_before_trx = chain_connection.get_wallet_balance(sender_obj.public_key)
            trx: dict = chain_connection.send_ether(
                uuid=data.get('uuid'),
                recipient_address=data.get('recipient'),
                amount=data.get('amount')
            )

            time.sleep(10)

            Transaction.objects.create(
                sender=sender_obj.public_key,
                receiver=data.get('recipient'),
                amount=data.get('amount'),
                balance_after_transaction=chain_connection.get_wallet_balance(sender_obj.public_key),
                transacting_currency="ETH",
                transaction_type="on-chain",
                hash=trx.get('tx_')
            )

            # update correct balance after 20sec delay
            amount_after_trx = chain_connection.get_wallet_balance(sender_obj.public_key)
            amount_diff = amount_before_trx - amount_after_trx
            sender_obj.previous_bal = sender_obj.previous_bal - amount_diff
            sender_obj.available_bal = sender_obj.available_bal - amount_diff
            sender_obj.save()

            return trx


class EthereumWalletDetails(RetrieveAPIView):
    permission_classes = [AnonPermissionOnly]
    queryset = Ethereum.objects.all()

    def get(self, *args, **kwargs):
        """
        1. check last sending off-chain/on-chain transaction
        2. get amount transferred and bal after transact
        3. add both figures
        4. check amount on the chain
        5. Subtract amount from segment-3 after the addition, from the value retrieved from chain
        6. add to the current previous and available balance
        :param args:
        :param kwargs:
        :return:
        """
        owner: Ethereum = Ethereum.objects.get(uuid=kwargs.get('uuid'))
        trx_qs = Transaction.objects.filter(sender=owner.public_key).order_by("-timestamp")
        recent_trx = trx_qs.first()
        last_bal = recent_trx.balance_after_transaction
        recent_bal = chain_connection.get_wallet_balance(owner.public_key)
        exact_amount_increase = recent_bal - last_bal
        print(exact_amount_increase)

        owner.previous_bal = owner.previous_bal + exact_amount_increase
        owner.available_bal = owner.available_bal + exact_amount_increase
        owner.save()

        details = {
            "address": owner.public_key,
            "available_balance": owner.available_bal,
            "frozen": owner.frozen,
            "frozen_bal": owner.frozen_bal,
            "uuid": owner.uuid,
            "name": owner.name,
            "short_name": owner.short_name,
            "icon": owner.icon
        }

        return Response(
            {"message": "retrieved", "data": details},
            status=status.HTTP_200_OK
        )


class USDTCreate(CreateAPIView):
    permission_classes = [AnonPermissionOnly]
    queryset = TetherUSD.objects.all()
    serializer_class = USDTSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class USDTTransfer(APIView):
    permission_classes = [AnonPermissionOnly]

    def post(self, *args, **kwargs):
        data = self.request.data
        try:
            TetherUSD.objects.get(public_key=data.get('recipient'))
            print("off-chain")

            # validation before transaction
            # perform off-chain transaction and hash the timestamp
            sender_obj = TetherUSD.objects.get(uuid=data.get('uuid'))
            if sender_obj.available_bal <= float(data.get('amount')):
                return Response(
                    {'message': "transaction failed due to insufficient balance"},
                    status=status.HTTP_402_PAYMENT_REQUIRED
                )
            sender_obj.previous_bal = float(sender_obj.previous_bal) - float(data.get('amount'))
            sender_obj.available_bal = float(sender_obj.available_bal) - float(data.get('amount'))
            sender_obj.save()

            recipient_obj = TetherUSD.objects.get(public_key=data.get('recipient'))
            recipient_obj.previous_bal = float(recipient_obj.previous_bal) + float(data.get('amount'))
            recipient_obj.available_bal = float(recipient_obj.available_bal) + float(data.get('amount'))
            recipient_obj.save()

            tx_hash = hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest()[:60]

            # record transaction
            Transaction.objects.create(
                sender=sender_obj.public_key,
                receiver=recipient_obj.public_key,
                amount=float(data.get('amount')),
                balance_after_transaction=sender_obj.available_bal,
                transacting_currency="USDT",
                transaction_type="off-chain",
                hash=f"0x{str(tx_hash)}".upper()
            )

            return Response(
                {
                    'message': "transaction successful",
                    "tx_": f"0x{str(tx_hash)}".upper(),
                    "success": bool(tx_hash)
                },
                status=status.HTTP_201_CREATED
            )
        except TetherUSD.DoesNotExist:
            print("on-chain")
            sender_obj = TetherUSD.objects.get(uuid=data.get('uuid'))
            if sender_obj.available_bal <= float(data.get('amount')):
                return Response(
                    {'message': "transaction failed due to insufficient balance"},
                    status=status.HTTP_402_PAYMENT_REQUIRED
                )
            # Does not exist/not a syarpa user perform on-chain transaction
            amount_before_trx = chain_connection.get_usdt_balance(sender_obj.public_key)
            trx: dict = chain_connection.send_usdt(
                uuid=data.get('uuid'),
                recipient_address=data.get('recipient'),
                amount=data.get('amount')
            )

            time.sleep(10)

            Transaction.objects.create(
                sender=sender_obj.public_key,
                receiver=data.get('recipient'),
                amount=data.get('amount'),
                balance_after_transaction=chain_connection.get_usdt_balance(sender_obj.public_key),
                transacting_currency="USDT",
                transaction_type="on-chain",
                hash=trx.get('tx_')
            )

            # update correct balance after 20sec delay
            amount_after_trx = chain_connection.get_usdt_balance(sender_obj.public_key)
            amount_diff = amount_before_trx - amount_after_trx
            sender_obj.previous_bal = sender_obj.previous_bal - amount_diff
            sender_obj.available_bal = sender_obj.available_bal - amount_diff
            sender_obj.save()

            return trx


class USDTWalletDetails(RetrieveAPIView):
    permission_classes = [AnonPermissionOnly]
    queryset = TetherUSD.objects.all()

    def get(self, *args, **kwargs):
        """
        1. check last sending off-chain/on-chain transaction
        2. get amount transferred and bal after transact
        3. add both figures
        4. check amount on the chain
        5. Subtract amount from segment-3 after the addition, from the value retrieved from chain
        6. add to the current previous and available balance
        :param args:
        :param kwargs:
        :return:
        """
        owner: TetherUSD = TetherUSD.objects.get(uuid=kwargs.get('uuid'))
        trx_qs = Transaction.objects.filter(sender=owner.public_key).order_by("-timestamp")
        recent_trx = trx_qs.first()
        last_bal = recent_trx.balance_after_transaction
        recent_bal = chain_connection.get_usdt_balance(owner.public_key)
        exact_amount_increase = recent_bal - last_bal
        print(exact_amount_increase)

        owner.previous_bal = owner.previous_bal + exact_amount_increase
        owner.available_bal = owner.available_bal + exact_amount_increase
        owner.save()

        details = {
            "address": owner.public_key,
            "available_balance": owner.available_bal,
            "frozen": owner.frozen,
            "frozen_bal": owner.frozen_bal,
            "uuid": owner.uuid,
            "name": owner.name,
            "short_name": owner.short_name,
            "icon": owner.icon
        }

        return Response(
            {"message": "retrieved", "data": details},
            status=status.HTTP_200_OK
        )


class BitcoinCreate(CreateAPIView):
    permission_classes = [AnonPermissionOnly]
    queryset = Bitcoin.objects.all()
    serializer_class = BitcoinSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
