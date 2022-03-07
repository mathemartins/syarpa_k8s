from django.urls import path, include

from wallet.api.views import EthereumCreate, EthereumTransfer

urlpatterns = [
    path('create/', EthereumCreate.as_view()),
    path('transfer/', EthereumTransfer.as_view())
]