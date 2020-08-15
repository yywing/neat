from normal import serializers, models
from utils import viewsets
# Create your views here.


class ParamViewSet(viewsets.NoCreateUpdateModelViewSet):
    queryset = models.Param.objects.all()
    serializer_class = serializers.ParamSerializer


class RawParamViewSet(viewsets.NoCreateUpdateModelViewSet):
    queryset = models.RawParam.objects.all()
    serializer_class = serializers.RawParamSerializer
