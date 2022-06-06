import json
from itertools import chain

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from syarpa_k8s.restconf.permissions import AnonPermissionOnly
from transaction.models import Transaction
from wallet.models import Ethereum


class TransactionEthereumListAPIView(APIView):
    permission_classes = [AnonPermissionOnly]

    def get(self, request, *args, **kwargs):
        wallet_instance: Ethereum = Ethereum.objects.get(uuid=kwargs.get('uuid'))
        address = wallet_instance.public_key
        sender_in_qs = Transaction.objects.filter(sender=address, transacting_currency="ETH")
        receiver_in_qs = Transaction.objects.filter(receiver=address, transacting_currency="ETH")
        qs = sender_in_qs | receiver_in_qs
        return Response(qs.values(), status=status.HTTP_200_OK)