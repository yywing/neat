from raw import serializers, models
from utils import viewsets
# Create your views here.


class RawViewSet(viewsets.NoUpdateModelViewSet):
    queryset = models.Raw.objects.all()
    serializer_class = serializers.RawSerializer


class UrlViewSet(viewsets.NoCreateUpdateModelViewSet):
    queryset = models.Url.objects.all()
    serializer_class = serializers.UrlSerializer


class RequestViewSet(viewsets.NoCreateUpdateModelViewSet):
    queryset = models.Request.objects.all()
    serializer_class = serializers.RequestSerializer


class ResponseViewSet(viewsets.NoCreateUpdateModelViewSet):
    queryset = models.Response.objects.all()
    serializer_class = serializers.ResponseSerializer
