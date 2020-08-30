from rest_framework import serializers

from raw import models
from utils.http import parse_request
from utils.rest.fields import Base64CharField


class RawSerializer(serializers.ModelSerializer):
    raw_request = Base64CharField(max_length=5 * 1024)
    raw_response = Base64CharField(max_length=1024 * 1024, required=False)

    class Meta:
        model = models.Raw
        fields = '__all__'
        read_only_fields = ['url']

    def create(self, validated_data):
        request = parse_request(
            validated_data['scheme'],
            validated_data['host'],
            validated_data['port'],
            validated_data['raw_request'],
        )
        u = models.Url.from_request(request)
        validated_data["url_id"] = u.id
        return super().create(validated_data)


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
