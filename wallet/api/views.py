import hashlib
import os
import time

import cryptocompare
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from syarpa_k8s.restconf.permissions import AnonPermissionOnly
from transaction.models import Transaction
from wallet.api.serializers import EthereumSerializer, USDTSerializer, BinanceCoinSerializer
from wallet.api.utils import EtherChain, get_mnemonic_seed_phrase, create_ledger_account, get_address, \
    activate_transaction_alert, transfer, BinanceSmartChain
from wallet.models import Ethereum, TetherUSD, BitcoinMnemonics, LedgerAccount, Address, BinanceCoin

chain_connection = EtherChain(infura_endpoint=os.environ.get('INFURA_ENDPOINT'))
bsc_chain_connection = BinanceSmartChain(bsc_endpoint=os.environ.get('BINANCE_SMARTCHAIN'))


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
        trx_qs: QuerySet = Transaction.objects.filter(sender=owner.public_key).order_by("-timestamp")
        print(trx_qs)
        if trx_qs.exists():
            recent_trx = trx_qs.first()
            last_bal = recent_trx.balance_after_transaction
            recent_bal = chain_connection.get_wallet_balance(owner.public_key)
            exact_amount_increase = recent_bal - last_bal
            print(exact_amount_increase)

            owner.previous_bal = owner.previous_bal + exact_amount_increase
            owner.available_bal = owner.available_bal + exact_amount_increase
            owner.save()

            price = cryptocompare.get_price('ETH', 'USD')
            current_price_in_usd = price.get('ETH')['USD']
            usd_price = current_price_in_usd * float(owner.available_bal)

            details = {
                "address": owner.public_key,
                "available_balance": owner.available_bal,
                "balance_in_usd": usd_price,
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
        last_bal = 0
        recent_bal = chain_connection.get_wallet_balance(owner.public_key)
        exact_amount_increase = recent_bal - last_bal
        print(exact_amount_increase)

        owner.previous_bal = owner.previous_bal + exact_amount_increase
        owner.available_bal = owner.available_bal + exact_amount_increase
        owner.save()

        price = cryptocompare.get_price('ETH', 'USD')
        current_price_in_usd = price.get('ETH')['USD']
        usd_price = current_price_in_usd * float(owner.available_bal)

        details = {
            "address": owner.public_key,
            "available_balance": owner.available_bal,
            "balance_in_usd": usd_price,
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
        trx_qs: QuerySet = Transaction.objects.filter(sender=owner.public_key).order_by("-timestamp")
        print(trx_qs)
        if trx_qs.exists():
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
                "balance_in_usd": owner.available_bal,
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
        last_bal = 0
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


class BinanceCreate(CreateAPIView):
    permission_classes = [AnonPermissionOnly]
    queryset = BinanceCoin.objects.all()
    serializer_class = BinanceCoinSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class BinanceTransfer(APIView):
    permission_classes = [AnonPermissionOnly]

    def post(self, *args, **kwargs):
        data = self.request.data
        try:
            BinanceCoin.objects.get(public_key=data.get('recipient'))
            print("off-chain")

            # validation before transaction
            # perform off-chain transaction and hash the timestamp
            sender_obj = BinanceCoin.objects.get(uuid=data.get('uuid'))
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
                transacting_currency="BNB",
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
        except BinanceCoin.DoesNotExist:
            print("on-chain")
            sender_obj = BinanceCoin.objects.get(uuid=data.get('uuid'))
            if sender_obj.available_bal <= float(data.get('amount')):
                return Response(
                    {'message': "transaction failed due to insufficient balance"},
                    status=status.HTTP_402_PAYMENT_REQUIRED
                )
            # Does not exist/not a syarpa user perform on-chain transaction
            amount_before_trx = bsc_chain_connection.get_wallet_balance(sender_obj.public_key)
            trx: dict = bsc_chain_connection.send_bnb(
                uuid=data.get('uuid'),
                recipient_address=data.get('recipient'),
                amount=data.get('amount')
            )

            time.sleep(10)

            Transaction.objects.create(
                sender=sender_obj.public_key,
                receiver=data.get('recipient'),
                amount=data.get('amount'),
                balance_after_transaction=bsc_chain_connection.get_wallet_balance(sender_obj.public_key),
                transacting_currency="BNB",
                transaction_type="on-chain",
                hash=trx.get('tx_')
            )

            # update correct balance after 20sec delay
            amount_after_trx = bsc_chain_connection.get_wallet_balance(sender_obj.public_key)
            amount_diff = amount_before_trx - amount_after_trx
            sender_obj.previous_bal = sender_obj.previous_bal - amount_diff
            sender_obj.available_bal = sender_obj.available_bal - amount_diff
            sender_obj.save()

            return trx


class BinanceWalletDetails(RetrieveAPIView):
    permission_classes = [AnonPermissionOnly]
    queryset = BinanceCoin.objects.all()

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
        owner: BinanceCoin = BinanceCoin.objects.get(uuid=kwargs.get('uuid'))
        trx_qs: QuerySet = Transaction.objects.filter(sender=owner.public_key).order_by("-timestamp")
        print(trx_qs)
        if trx_qs.exists():
            recent_trx = trx_qs.first()
            last_bal = recent_trx.balance_after_transaction
            recent_bal = chain_connection.get_wallet_balance(owner.public_key)
            exact_amount_increase = recent_bal - last_bal
            print(exact_amount_increase)

            owner.previous_bal = owner.previous_bal + exact_amount_increase
            owner.available_bal = owner.available_bal + exact_amount_increase
            owner.save()

            price = cryptocompare.get_price('BNB', 'USD')
            current_price_in_usd = price.get('BNB')['USD']
            usd_price = current_price_in_usd * float(owner.available_bal)

            details = {
                "address": owner.public_key,
                "available_balance": owner.available_bal,
                "balance_in_usd": usd_price,
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
        last_bal = 0
        recent_bal = chain_connection.get_wallet_balance(owner.public_key)
        exact_amount_increase = recent_bal - last_bal
        print(exact_amount_increase)

        owner.previous_bal = owner.previous_bal + exact_amount_increase
        owner.available_bal = owner.available_bal + exact_amount_increase
        owner.save()

        price = cryptocompare.get_price('BNB', 'USD')
        current_price_in_usd = price.get('BNB')['USD']
        usd_price = current_price_in_usd * float(owner.available_bal)

        details = {
            "address": owner.public_key,
            "available_balance": owner.available_bal,
            "balance_in_usd": usd_price,
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


class BitcoinCreate(APIView):
    permission_classes = [AnonPermissionOnly]

    def post(self, *args, **kwargs):
        data: dict = self.request.data
        user_seed: dict = get_mnemonic_seed_phrase(coin="bitcoin")
        bitcoin_mnemonics_obj = BitcoinMnemonics.objects.create(
            uuid=data.get('uuid'),
            seed_phrase=user_seed.get("mnemonic"),
            xpub=user_seed.get("xpub")
        )

        ledger_account: dict = create_ledger_account(coin_symbol="BTC", xpub=user_seed.get("xpub"))
        LedgerAccount.objects.create(
            coin_symbol=ledger_account.get("currency"),
            available_balance=ledger_account.get("balance")["availableBalance"],
            account_balance=ledger_account.get("balance")["accountBalance"],
            xpub=bitcoin_mnemonics_obj,
            customer_id=ledger_account.get("customerId"),
            ledger_id=ledger_account.get("id"),
        )

        address: dict = get_address(ledger_account.get("id"))
        public_key_obj = Address.objects.create(
            xpub=bitcoin_mnemonics_obj,
            derivation_key=address.get("derivationKey"),
            address_key=address.get("address"),
            coin_symbol=address.get("currency")
        )

        # Activate Transaction alert on system
        activate_transaction_alert(public_key_obj.address_key, public_key_obj.coin_symbol)

        return Response(
            {
                "message": "successful",
                "success": True,
                "data": {
                    "mnemonic": user_seed.get("mnemonic"),
                    "xpub": user_seed.get("xpub"),
                    "coin_symbol": ledger_account.get("currency"),
                    "address_public_key": address.get("address"),
                    "availableBalance": ledger_account.get("balance")["availableBalance"],
                    "accountBalance": ledger_account.get("balance")["accountBalance"],
                    "customer_id": ledger_account.get("customerId"),
                    "ledger_id": ledger_account.get("id"),
                    "active": True,
                    "frozen": False
                }
            },
            status=status.HTTP_201_CREATED
        )


class BitcoinWalletDetail(APIView):
    permission_classes = [AnonPermissionOnly]

    def get(self, *args, **kwargs):
        print(kwargs)
        owner = BitcoinMnemonics.objects.get(uuid=kwargs.get('uuid'))
        owner_ledger = LedgerAccount.objects.get(xpub=owner)
        owner_address = Address.objects.get(xpub=owner)

        price = cryptocompare.get_price('BTC', 'USD')
        current_price_in_usd = price.get('BTC')['USD']
        print(owner_ledger.available_balance)
        usd_price = current_price_in_usd * float(owner_ledger.available_balance)

        details = {
            "address": owner_address.address_key,
            "available_balance": owner_ledger.available_balance,
            "balance_in_usd": usd_price,
            "frozen": owner_ledger.frozen,
            "uuid": owner.uuid,
            "name": "Bitcoin",
            "coin_symbol": owner_ledger.coin_symbol,
            "icon": "",
        }

        return Response(
            {"message": "retrieved", "data": details},
            status=status.HTTP_200_OK
        )


class BitcoinWalletTransfer(APIView):
    permission_classes = [AnonPermissionOnly]

    def post(self, *args, **kwargs):
        data: dict = self.request.data
        owner: BitcoinMnemonics = BitcoinMnemonics.objects.get(uuid=data.get('uuid'))
        owner_ledger: LedgerAccount = LedgerAccount.objects.get(xpub=owner)
        owner_address = Address.objects.get(xpub=owner)

        return transfer(
            coin='bitcoin', ledger_id=owner_ledger.ledger_id,
            address=owner_address.address_key, amount=data.get('amount'),
            seed_phrase=owner.seed_phrase, xpub=owner.xpub
        )
