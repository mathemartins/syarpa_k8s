from django.conf.urls import url

from .views import FiatRateAPIView, FiatListView

urlpatterns = [
    url(r'^$', FiatRateAPIView.as_view(), name='list'),
    url(r'^data/$', FiatListView.as_view(), name='data-list'),
]