from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from syarpa_k8s.mixins import IsConnected
from syarpa_k8s.restconf.permissions import AnonPermissionOnly
from wallet.api.serializers import EthereumSerializer
from wallet.models import Ethereum


class EthereumCreate(CreateAPIView):
    permission_classes = [AnonPermissionOnly]
    queryset = Ethereum.objects.all()
    serializer_class = EthereumSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}