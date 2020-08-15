from rest_framework import serializers

from raw import models


class RawSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Raw
        fields = '__all__'
        read_only_fields = ['url']


class UrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Url
        fields = '__all__'
        read_only_fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Request
        fields = '__all__'
        read_only_fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Response
        fields = '__all__'
        read_only_fields = '__all__'
