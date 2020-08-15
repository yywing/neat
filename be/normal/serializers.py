from rest_framework import serializers

from normal import models


class ParamSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Param
        fields = '__all__'
        read_only_fields = '__all__'


class RawParamSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RawParam
        fields = '__all__'
        read_only_fields = '__all__'
