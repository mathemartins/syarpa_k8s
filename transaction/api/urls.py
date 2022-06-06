from django.urls import path

from transaction.api.views import (
    TransactionEthereumListAPIView
)

urlpatterns = [
    path('transactions/<slug:uuid>/ethereum/', TransactionEthereumListAPIView.as_view()),
]