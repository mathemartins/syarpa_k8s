from django.urls import path, include

from wallet.api.views import (
    EthereumCreate, EthereumTransfer, EthereumWalletDetails, USDTCreate,
    USDTTransfer, USDTWalletDetails, BitcoinCreate
)

urlpatterns = [
    path('create/ethereum/', EthereumCreate.as_view()),
    path('transfer/ethereum/', EthereumTransfer.as_view()),
    path('details/<slug:uuid>/ethereum/', EthereumWalletDetails.as_view()),

    path('create/usdt/', USDTCreate.as_view()),
    path('transfer/usdt', USDTTransfer.as_view()),
    path('details/<slug:uuid>/usdt', USDTWalletDetails.as_view()),

    path('create/bitcoin', BitcoinCreate.as_view()),
]