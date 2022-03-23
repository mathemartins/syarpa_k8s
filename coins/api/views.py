from rest_framework.generics import ListAPIView

from coins.api.serializers import CoinSerializer
from coins.models import Coin
from syarpa_k8s.restconf.permissions import AnonPermissionOnly


class CoinListAPIView(ListAPIView):
    serializer_class = CoinSerializer
    permission_classes = [AnonPermissionOnly]
    queryset = Coin.objects.all().order_by('pk')
    paginate_by = 500