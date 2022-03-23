import os

from rest_framework import status
from rest_framework.response import Response
from time import sleep
from web3 import Web3

from wallet.models import Ethereum


class EtherChain:
    def __init__(self, infura_endpoint=os.environ.get('INFURA_ENDPOINT')):
        self.infura_endpoint = infura_endpoint

    def create_wallet(self):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            return web3.eth.account.create()
        return Response({"message": "You are connected to the blockchain"}, status=status.HTTP_400_BAD_REQUEST)

    def get_gas_price(self):
        import requests
        url = "https://ethgasstation.info/api/ethgasAPI.json?api-key" \
              "=3d8d6fc803ee423ffe629e5d50689a72da4b67c2b975fe058f9e2bd11020 "
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def get_gas_price_web3(self):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            return web3.eth.gas_price
        return Response({"message": "You are connected to the blockchain"}, status=status.HTTP_400_BAD_REQUEST)

    def get_wallet_balance(self, address: str):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            balance = web3.eth.get_balance(address)
            return web3.fromWei(balance, 'ether')

    def get_trx_information(self, trx_hash):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            return web3.eth.get_transaction(transaction_hash=trx_hash)

    def send_ether(self, uuid: str, recipient_address: str, amount):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            sender_obj = Ethereum.objects.get(uuid=uuid)
            gas_price = float(self.get_gas_price().get("fast")) / 10
            dc_private_key = web3.eth.account.decrypt(
                keyfile_json=sender_obj.encrypted_private_key,
                password=sender_obj.uuid
            )
            nonce = web3.eth.getTransactionCount(sender_obj.public_key)
            tx = {
                'nonce': nonce,
                'to': recipient_address,
                'value': web3.toWei(amount, 'ether'),
                'gas': 21000,
                'gasPrice': web3.toWei('{gasPrice}'.format(gasPrice=gas_price), 'gwei')
            }
            signed_transaction = web3.eth.account.signTransaction(
                tx, dc_private_key
            )
            tx_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

            # waits for 5 seconds before updating balance
            sleep(10)

            return Response(
                {
                    'message': "transaction successful",
                    "tx_": web3.toHex(tx_hash),
                    "success": bool(web3.toHex(tx_hash))
                },
                status=status.HTTP_201_CREATED
            )
        return Response({"message": "You are connected to the blockchain"}, status=status.HTTP_400_BAD_REQUEST)

    def send_usdt(self, uuid: str, recipient_address: str, amount):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            pass
        return Response({"message": "You are connected to the blockchain"}, status=status.HTTP_400_BAD_REQUEST)

