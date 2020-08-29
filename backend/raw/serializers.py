from rest_framework import serializers

from raw import models
from utils.rest.fields import Base64CharField


class RawSerializer(serializers.ModelSerializer):
    raw_request = Base64CharField(max_length=5 * 1024)
    raw_response = Base64CharField(max_length=1024 * 1024, required=False)

    class Meta:
        model = models.Raw
        fields = '__all__'
        read_only_fields = ['url']


class UrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Url
        fields = '__all__'
        # view control
        # read_only_fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Request
        fields = '__all__'
        # view control
        # read_only_fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Response
        fields = '__all__'
        # view control
        # read_only_fields = '__all__'
