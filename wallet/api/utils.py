import os

from rest_framework import status
from rest_framework.response import Response
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

    def send_ether(self, uuid, recipient_address, amount):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            sender_obj = Ethereum.objects.get(uuid=uuid)
            gas_price = 2100
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
            sender_obj.previous_bal = float(sender_obj.previous_bal) - float(amount)
            sender_obj.available = float(sender_obj.available) - float(amount)
            sender_obj.save()

            return Response(
                {
                    'message': "transaction successful",
                    "tx_": web3.toHex(tx_hash),
                    "success": bool(web3.toHex(tx_hash))
                },
                status=status.HTTP_201_CREATED
            )
