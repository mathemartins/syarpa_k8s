from django.urls import path

from coins.api.views import CoinListAPIView

urlpatterns = [
    path('', CoinListAPIView.as_view(), name='coin-list'),
]