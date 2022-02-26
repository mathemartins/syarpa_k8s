from django.urls import path, include

from wallet.api.views import EthereumCreate

urlpatterns = [
    path('create/', EthereumCreate.as_view()),
]