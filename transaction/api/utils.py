import os

from web3 import Web3


class TransactionChecker:
    web3 = None
    web3ws = None
    account = None
    subscription = None

    def __init__(self, account: str):
        self.web3 = Web3(Web3.HTTPProvider(os.environ.get('INFURA_ENDPOINT')))
        self.web3ws = Web3(Web3.WebsocketProvider(os.environ.get('INFURA_WS')))
        self.account = account.lower()

    def subscribe(self, topic):
        self.subscription = self.web3ws.eth.subscribe(topic)

    async def watch_transaction(self, txHash):
        print("watching transaction")
        if self.subscription:
            tx = await self.web3.eth.getTransaction(txHash)
            if tx is not None and self.account == tx.to.lower():
                output_dict: dict = {
                    'address': tx.address,
                    'value': self.web3.fromWei(tx.value, 'ether')
                }
                print(output_dict)
