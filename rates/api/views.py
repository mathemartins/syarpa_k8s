from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rates.api.serializers import FiatRateListSerializer
from rates.models import FiatRate


class FiatRateAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def get(self, request):
        try:
            user_profile_obj = Profile.objects.get(user=request.user)
            user_country = FiatRate.objects.get(country=user_profile_obj.country)
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'status code': status_code,
                'message': 'User Fiat Fetched',
                'data': [{
                    'updated': user_country.updated,
                    'timestamp': user_country.timestamp,
                    'country': user_profile_obj.get_country(),
                    'dollar_rate': user_country.dollar_rate
                }]
            }

        except Exception as e:
            user_profile_obj = Profile.objects.get(user=request.user)
            user_country = FiatRate.objects.get(country='United States Of America')
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'status code': status_code,
                'message': 'User Fiat Fetched',
                'data': [{
                    'updated': user_country.updated,
                    'timestamp': user_country.timestamp,
                    'country': user_profile_obj.get_country(),
                    'dollar_rate': user_country.dollar_rate
                }]
            }
        return Response(response, status=status_code)


class FiatListView(ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    serializer_class = FiatRateListSerializer
    queryset = FiatRate.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    paginate_by = 15