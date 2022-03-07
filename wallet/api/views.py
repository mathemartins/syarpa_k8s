import hashlib
import os
import time

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from syarpa_k8s.restconf.permissions import AnonPermissionOnly
from wallet.api.serializers import EthereumSerializer
from wallet.api.utils import EtherChain
from wallet.models import Ethereum

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
        if exists := Ethereum.objects.get(public_key=data.get('recipient')):
            # perform off-chain transaction and hash the timestamp
            sender_obj = Ethereum.objects.get(uuid=data.get('uuid'))
            sender_obj.previous_bal = float(sender_obj.previous_bal) - float(data.get('amount'))
            sender_obj.available = float(sender_obj.available) - float(data.get('amount'))
            sender_obj.save()

            recipient_obj = Ethereum.objects.get(public_key=data.get('recipient'))
            recipient_obj.previous_bal = float(recipient_obj.previous_bal) + float(data.get('amount'))
            recipient_obj.available = float(recipient_obj.available) + float(data.get('amount'))
            recipient_obj.save()

            hash_ = hashlib.sha1()
            hash_.update(str(time.time()))
            tx_hash = hash_.hexdigest()[:15]

            return Response(
                {
                    'message': "transaction successful",
                    "tx_": tx_hash,
                    "success": bool(tx_hash)
                },
                status=status.HTTP_201_CREATED
            )
        return chain_connection.send_ether(
            uuid=data.get('uuid'),
            recipient_address=data.get('recipient'),
            amount=data.get('amount')
        )




