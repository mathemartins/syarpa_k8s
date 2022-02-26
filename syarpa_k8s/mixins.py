import os

from rest_framework.response import Response
from web3 import Web3


class IsConnected(object):
    def dispatch(self, request, *args, **kwargs):
        web3 = Web3(Web3.HTTPProvider(os.environ.get("INFURA_ENDPOINT")))
        if not web3.isConnected():
            return Response({"message": "Oops! Not connected to the blockchain"}, status=403)