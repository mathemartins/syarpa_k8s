import json
import os

import requests
from rest_framework import status
from rest_framework.response import Response
from time import sleep
from web3 import Web3

from syarpa_k8s.settings import BASE_DIR
from wallet.models import Ethereum, TetherUSD, Bitcoin


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

            # waits for 10 seconds before updating balance
            sleep(10)

            return Response(
                {
                    'message': "transaction successful",
                    "tx_": web3.toHex(tx_hash),
                    "success": bool(web3.toHex(tx_hash))
                },
                status=status.HTTP_201_CREATED
            )
        return Response({"message": "You are not connected to the blockchain"}, status=status.HTTP_400_BAD_REQUEST)

    def send_usdt(self, uuid: str, recipient_address: str, amount):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            sender_obj = TetherUSD.objects.get(uuid=uuid)
            gas_price = float(self.get_gas_price().get("fast")) / 10
            dc_private_key = web3.eth.account.decrypt(
                keyfile_json=sender_obj.encrypted_private_key,
                password=sender_obj.uuid
            )
            usdt_contract_address = Web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')
            usdt_contract_abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"",'
                                           '"type":"string"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":false,"inputs":[{'
                                           '"name":"_upgradedAddress","type":"address"}],"name":"deprecate",'
                                           '"outputs":[],"payable":false,"stateMutability":"nonpayable",'
                                           '"type":"function"},{"constant":false,"inputs":[{"name":"_spender",'
                                           '"type":"address"},{"name":"_value","type":"uint256"}],"name":"approve",'
                                           '"outputs":[],"payable":false,"stateMutability":"nonpayable",'
                                           '"type":"function"},{"constant":true,"inputs":[],"name":"deprecated",'
                                           '"outputs":[{"name":"","type":"bool"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{'
                                           '"name":"_evilUser","type":"address"}],"name":"addBlackList","outputs":[],'
                                           '"payable":false,"stateMutability":"nonpayable","type":"function"},'
                                           '{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"",'
                                           '"type":"uint256"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":false,"inputs":[{"name":"_from",'
                                           '"type":"address"},{"name":"_to","type":"address"},{"name":"_value",'
                                           '"type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,'
                                           '"stateMutability":"nonpayable","type":"function"},{"constant":true,'
                                           '"inputs":[],"name":"upgradedAddress","outputs":[{"name":"",'
                                           '"type":"address"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":true,"inputs":[{"name":"",'
                                           '"type":"address"}],"name":"balances","outputs":[{"name":"",'
                                           '"type":"uint256"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":true,"inputs":[],"name":"decimals",'
                                           '"outputs":[{"name":"","type":"uint256"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],'
                                           '"name":"maximumFee","outputs":[{"name":"","type":"uint256"}],'
                                           '"payable":false,"stateMutability":"view","type":"function"},'
                                           '{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"",'
                                           '"type":"uint256"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":false,"inputs":[],"name":"unpause",'
                                           '"outputs":[],"payable":false,"stateMutability":"nonpayable",'
                                           '"type":"function"},{"constant":true,"inputs":[{"name":"_maker",'
                                           '"type":"address"}],"name":"getBlackListStatus","outputs":[{"name":"",'
                                           '"type":"bool"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":true,"inputs":[{"name":"",'
                                           '"type":"address"},{"name":"","type":"address"}],"name":"allowed",'
                                           '"outputs":[{"name":"","type":"uint256"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],'
                                           '"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{'
                                           '"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"",'
                                           '"type":"uint256"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":false,"inputs":[],"name":"pause",'
                                           '"outputs":[],"payable":false,"stateMutability":"nonpayable",'
                                           '"type":"function"},{"constant":true,"inputs":[],"name":"getOwner",'
                                           '"outputs":[{"name":"","type":"address"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],'
                                           '"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],'
                                           '"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{'
                                           '"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],'
                                           '"name":"transfer","outputs":[],"payable":false,'
                                           '"stateMutability":"nonpayable","type":"function"},{"constant":false,'
                                           '"inputs":[{"name":"newBasisPoints","type":"uint256"},{"name":"newMaxFee",'
                                           '"type":"uint256"}],"name":"setParams","outputs":[],"payable":false,'
                                           '"stateMutability":"nonpayable","type":"function"},{"constant":false,'
                                           '"inputs":[{"name":"amount","type":"uint256"}],"name":"issue","outputs":['
                                           '],"payable":false,"stateMutability":"nonpayable","type":"function"},'
                                           '{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],'
                                           '"name":"redeem","outputs":[],"payable":false,'
                                           '"stateMutability":"nonpayable","type":"function"},{"constant":true,'
                                           '"inputs":[{"name":"_owner","type":"address"},{"name":"_spender",'
                                           '"type":"address"}],"name":"allowance","outputs":[{"name":"remaining",'
                                           '"type":"uint256"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":true,"inputs":[],"name":"basisPointsRate",'
                                           '"outputs":[{"name":"","type":"uint256"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{'
                                           '"name":"","type":"address"}],"name":"isBlackListed","outputs":[{'
                                           '"name":"","type":"bool"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":false,"inputs":[{"name":"_clearedUser",'
                                           '"type":"address"}],"name":"removeBlackList","outputs":[],"payable":false,'
                                           '"stateMutability":"nonpayable","type":"function"},{"constant":true,'
                                           '"inputs":[],"name":"MAX_UINT","outputs":[{"name":"","type":"uint256"}],'
                                           '"payable":false,"stateMutability":"view","type":"function"},'
                                           '{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],'
                                           '"name":"transferOwnership","outputs":[],"payable":false,'
                                           '"stateMutability":"nonpayable","type":"function"},{"constant":false,'
                                           '"inputs":[{"name":"_blackListedUser","type":"address"}],'
                                           '"name":"destroyBlackFunds","outputs":[],"payable":false,'
                                           '"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
                                           '"name":"_initialSupply","type":"uint256"},{"name":"_name",'
                                           '"type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals",'
                                           '"type":"uint256"}],"payable":false,"stateMutability":"nonpayable",'
                                           '"type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,'
                                           '"name":"amount","type":"uint256"}],"name":"Issue","type":"event"},'
                                           '{"anonymous":false,"inputs":[{"indexed":false,"name":"amount",'
                                           '"type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":false,'
                                           '"inputs":[{"indexed":false,"name":"newAddress","type":"address"}],'
                                           '"name":"Deprecate","type":"event"},{"anonymous":false,"inputs":[{'
                                           '"indexed":false,"name":"feeBasisPoints","type":"uint256"},'
                                           '{"indexed":false,"name":"maxFee","type":"uint256"}],"name":"Params",'
                                           '"type":"event"},{"anonymous":false,"inputs":[{"indexed":false,'
                                           '"name":"_blackListedUser","type":"address"},{"indexed":false,'
                                           '"name":"_balance","type":"uint256"}],"name":"DestroyedBlackFunds",'
                                           '"type":"event"},{"anonymous":false,"inputs":[{"indexed":false,'
                                           '"name":"_user","type":"address"}],"name":"AddedBlackList",'
                                           '"type":"event"},{"anonymous":false,"inputs":[{"indexed":false,'
                                           '"name":"_user","type":"address"}],"name":"RemovedBlackList",'
                                           '"type":"event"},{"anonymous":false,"inputs":[{"indexed":true,'
                                           '"name":"owner","type":"address"},{"indexed":true,"name":"spender",'
                                           '"type":"address"},{"indexed":false,"name":"value","type":"uint256"}],'
                                           '"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{'
                                           '"indexed":true,"name":"from","type":"address"},{"indexed":true,'
                                           '"name":"to","type":"address"},{"indexed":false,"name":"value",'
                                           '"type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,'
                                           '"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,'
                                           '"inputs":[],"name":"Unpause","type":"event"}]')
            usdt_contract = web3.eth.contract(address=usdt_contract_address, abi=usdt_contract_abi)
            sender_address = Web3.toChecksumAddress(sender_obj.public_key)

            nonce = web3.eth.getTransactionCount(sender_address)
            tx = usdt_contract.functions.transfer(recipient_address, web3.toWei(amount, 'ether')).buildTransaction({
                'gas': 21000,
                'gasPrice': web3.toWei('{gasPrice}'.format(gasPrice=gas_price), 'gwei'),
                'nonce': nonce
            })
            signed_tx = web3.eth.account.signTransaction(tx, private_key=dc_private_key)
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

            # waits for 10 seconds before updating balance
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

    def get_usdt_balance(self, address: str):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            usdt_contract_address = Web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')
            usdt_contract_abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"",'
                                           '"type":"string"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":false,"inputs":[{'
                                           '"name":"_upgradedAddress","type":"address"}],"name":"deprecate",'
                                           '"outputs":[],"payable":false,"stateMutability":"nonpayable",'
                                           '"type":"function"},{"constant":false,"inputs":[{"name":"_spender",'
                                           '"type":"address"},{"name":"_value","type":"uint256"}],"name":"approve",'
                                           '"outputs":[],"payable":false,"stateMutability":"nonpayable",'
                                           '"type":"function"},{"constant":true,"inputs":[],"name":"deprecated",'
                                           '"outputs":[{"name":"","type":"bool"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{'
                                           '"name":"_evilUser","type":"address"}],"name":"addBlackList","outputs":[],'
                                           '"payable":false,"stateMutability":"nonpayable","type":"function"},'
                                           '{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"",'
                                           '"type":"uint256"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":false,"inputs":[{"name":"_from",'
                                           '"type":"address"},{"name":"_to","type":"address"},{"name":"_value",'
                                           '"type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,'
                                           '"stateMutability":"nonpayable","type":"function"},{"constant":true,'
                                           '"inputs":[],"name":"upgradedAddress","outputs":[{"name":"",'
                                           '"type":"address"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":true,"inputs":[{"name":"",'
                                           '"type":"address"}],"name":"balances","outputs":[{"name":"",'
                                           '"type":"uint256"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":true,"inputs":[],"name":"decimals",'
                                           '"outputs":[{"name":"","type":"uint256"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],'
                                           '"name":"maximumFee","outputs":[{"name":"","type":"uint256"}],'
                                           '"payable":false,"stateMutability":"view","type":"function"},'
                                           '{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"",'
                                           '"type":"uint256"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":false,"inputs":[],"name":"unpause",'
                                           '"outputs":[],"payable":false,"stateMutability":"nonpayable",'
                                           '"type":"function"},{"constant":true,"inputs":[{"name":"_maker",'
                                           '"type":"address"}],"name":"getBlackListStatus","outputs":[{"name":"",'
                                           '"type":"bool"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":true,"inputs":[{"name":"",'
                                           '"type":"address"},{"name":"","type":"address"}],"name":"allowed",'
                                           '"outputs":[{"name":"","type":"uint256"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],'
                                           '"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{'
                                           '"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"",'
                                           '"type":"uint256"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":false,"inputs":[],"name":"pause",'
                                           '"outputs":[],"payable":false,"stateMutability":"nonpayable",'
                                           '"type":"function"},{"constant":true,"inputs":[],"name":"getOwner",'
                                           '"outputs":[{"name":"","type":"address"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],'
                                           '"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],'
                                           '"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{'
                                           '"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],'
                                           '"name":"transfer","outputs":[],"payable":false,'
                                           '"stateMutability":"nonpayable","type":"function"},{"constant":false,'
                                           '"inputs":[{"name":"newBasisPoints","type":"uint256"},{"name":"newMaxFee",'
                                           '"type":"uint256"}],"name":"setParams","outputs":[],"payable":false,'
                                           '"stateMutability":"nonpayable","type":"function"},{"constant":false,'
                                           '"inputs":[{"name":"amount","type":"uint256"}],"name":"issue","outputs":['
                                           '],"payable":false,"stateMutability":"nonpayable","type":"function"},'
                                           '{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],'
                                           '"name":"redeem","outputs":[],"payable":false,'
                                           '"stateMutability":"nonpayable","type":"function"},{"constant":true,'
                                           '"inputs":[{"name":"_owner","type":"address"},{"name":"_spender",'
                                           '"type":"address"}],"name":"allowance","outputs":[{"name":"remaining",'
                                           '"type":"uint256"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":true,"inputs":[],"name":"basisPointsRate",'
                                           '"outputs":[{"name":"","type":"uint256"}],"payable":false,'
                                           '"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{'
                                           '"name":"","type":"address"}],"name":"isBlackListed","outputs":[{'
                                           '"name":"","type":"bool"}],"payable":false,"stateMutability":"view",'
                                           '"type":"function"},{"constant":false,"inputs":[{"name":"_clearedUser",'
                                           '"type":"address"}],"name":"removeBlackList","outputs":[],"payable":false,'
                                           '"stateMutability":"nonpayable","type":"function"},{"constant":true,'
                                           '"inputs":[],"name":"MAX_UINT","outputs":[{"name":"","type":"uint256"}],'
                                           '"payable":false,"stateMutability":"view","type":"function"},'
                                           '{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],'
                                           '"name":"transferOwnership","outputs":[],"payable":false,'
                                           '"stateMutability":"nonpayable","type":"function"},{"constant":false,'
                                           '"inputs":[{"name":"_blackListedUser","type":"address"}],'
                                           '"name":"destroyBlackFunds","outputs":[],"payable":false,'
                                           '"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
                                           '"name":"_initialSupply","type":"uint256"},{"name":"_name",'
                                           '"type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals",'
                                           '"type":"uint256"}],"payable":false,"stateMutability":"nonpayable",'
                                           '"type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,'
                                           '"name":"amount","type":"uint256"}],"name":"Issue","type":"event"},'
                                           '{"anonymous":false,"inputs":[{"indexed":false,"name":"amount",'
                                           '"type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":false,'
                                           '"inputs":[{"indexed":false,"name":"newAddress","type":"address"}],'
                                           '"name":"Deprecate","type":"event"},{"anonymous":false,"inputs":[{'
                                           '"indexed":false,"name":"feeBasisPoints","type":"uint256"},'
                                           '{"indexed":false,"name":"maxFee","type":"uint256"}],"name":"Params",'
                                           '"type":"event"},{"anonymous":false,"inputs":[{"indexed":false,'
                                           '"name":"_blackListedUser","type":"address"},{"indexed":false,'
                                           '"name":"_balance","type":"uint256"}],"name":"DestroyedBlackFunds",'
                                           '"type":"event"},{"anonymous":false,"inputs":[{"indexed":false,'
                                           '"name":"_user","type":"address"}],"name":"AddedBlackList",'
                                           '"type":"event"},{"anonymous":false,"inputs":[{"indexed":false,'
                                           '"name":"_user","type":"address"}],"name":"RemovedBlackList",'
                                           '"type":"event"},{"anonymous":false,"inputs":[{"indexed":true,'
                                           '"name":"owner","type":"address"},{"indexed":true,"name":"spender",'
                                           '"type":"address"},{"indexed":false,"name":"value","type":"uint256"}],'
                                           '"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{'
                                           '"indexed":true,"name":"from","type":"address"},{"indexed":true,'
                                           '"name":"to","type":"address"},{"indexed":false,"name":"value",'
                                           '"type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,'
                                           '"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,'
                                           '"inputs":[],"name":"Unpause","type":"event"}]')
            usdt_contract = web3.eth.contract(address=usdt_contract_address, abi=usdt_contract_abi)
            usdt_address = Web3.toChecksumAddress(address)
            usdt_balance = usdt_contract.functions.balanceOf(usdt_address).call()
            return web3.fromWei(usdt_balance, 'ether')


class OminiChain:
    def __init__(
            self,
            tatum_endpoint=os.environ.get('TATUM_API'),
            network_type=os.environ.get('TATUM_NETWORK_TYPE'),
            base_url=os.environ.get('TATUM_BASE_URL'),
    ):
        self.tatum_endpoint = tatum_endpoint
        self.network_type = network_type
        self.base_url = base_url

    def create_wallet(self):
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': f'{self.tatum_endpoint}',
        }
        params = {
            'type': f'{self.network_type}',
        }
        xpub_response = requests.get(f'{self.base_url}v3/bitcoin/wallet', headers=headers, params=params)
        xpub_response_dict: dict = json.loads(xpub_response.content.decode('utf-8'))
        address_response = requests.get(
            f'{self.base_url}v3/bitcoin/address/{xpub_response_dict.get("xpub")}/0',
            headers=headers, params=params
        )
        address_response_dict = json.loads(address_response.content.decode('utf-8'))
        json_data = {
            'index': 0,
            'mnemonic': f'{xpub_response_dict.get("mnemonic")}',
        }

        pk_response = requests.post(
            f'{self.base_url}/v3/bitcoin/wallet/priv', headers=headers, params=params,
            json=json_data
        )
        pk_response_dict: dict = json.loads(pk_response.content.decode('utf-8'))
        data = {
            "address": address_response_dict.get("address"),
            "mnemonic": xpub_response_dict.get("mnemonic"),
            "xpub": xpub_response_dict.get("xpub"),
            "private_key": pk_response_dict.get("key")
        }
        return Response(data=data, status=status.HTTP_200_OK)
