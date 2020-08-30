from django.db import models
from django.core import validators

from raw.constants import SchemeEnum, RequestMethodEnum, RequestTypeEnum, ResponseTypeEnum
from utils.http import (
    parse_request, parse_response,
    Request as RequestObject, Response as ResponseObject
)
# Create your models here.


class Raw(models.Model):

    SCHEME = tuple([
        (enum_item.value, enum_item.name)
        for enum_item in SchemeEnum.__members__.values()
    ])

    scheme = models.CharField(choices=SCHEME, max_length=255)
    host = models.CharField(max_length=255)
    port = models.IntegerField(validators=[validators.MaxValueValidator(65535), validators.MinValueValidator(1)])
    raw_request = models.BinaryField(max_length=5 * 1024, help_text="原始请求")
    raw_response = models.BinaryField(max_length=1024 * 1024, null=True, blank=False, help_text="原始响应")
    created_time = models.DateTimeField(auto_now_add=True)

    url = models.ForeignKey("Url", on_delete=models.CASCADE, related_name="raws")

    class Meta:
        ordering = ['-created_time', ]

    @property
    def request_object(self):
        return parse_request(self.scheme, self.host, self.port, self.raw_request)

    @property
    def response_object(self):
        return parse_response(self.raw_response, self.request)

    @property
    def url_str(self):
        return self.request_object.url

    @property
    def standard_url(self):
        return self.request_object.pure_url


class Url(models.Model):

    SCHEME = tuple([
        (enum_item.value, enum_item.name)
        for enum_item in SchemeEnum.__members__.values()
    ])

    scheme = models.CharField(choices=SCHEME, max_length=255, editable=False)
    host = models.CharField(max_length=255, editable=False)
    port = models.IntegerField(validators=[validators.MaxValueValidator(65535), validators.MinValueValidator(1)], editable=False)
    path = models.CharField(max_length=255, editable=False)
    url = models.CharField(max_length=255, editable=False, unique=True)
    suffix = models.CharField(max_length=255, editable=False)

    class Meta:
        ordering = ['url', ]

    @classmethod
    def from_request(cls, request: RequestObject):
        u, _ = cls.objects.get_or_create(
            url=request.pure_url,
            defaults=dict(
                scheme=request.scheme,
                host=request.host,
                port=request.port,
                path=request.path,
                suffix=request.suffix
            )
        )
        return u


class Request(models.Model):
    REQUEST_TYPE = tuple([
        (enum_item.value, enum_item.name)
        for enum_item in RequestTypeEnum.__members__.values()
    ])
    REQUEST_METHOD = tuple([
        (enum_item.value, enum_item.name)
        for enum_item in RequestMethodEnum.__members__.values()
    ])

    url = models.ForeignKey("Url", editable=False, on_delete=models.CASCADE, related_name="requests")
    raw = models.OneToOneField("Raw", on_delete=models.CASCADE, related_name="request")

    method = models.CharField(
        max_length=255,
        choices=REQUEST_METHOD,
        default=RequestMethodEnum.GET.value,
        help_text="请求方法"
    )
    request_headers = models.JSONField(editable=False, help_text="原始请求")
    request_body = models.BinaryField(max_length=5 * 1024, editable=False, help_text="请求 body")
    request_type = models.CharField(
        max_length=255,
        choices=REQUEST_TYPE,
        default=RequestTypeEnum.NORMAL.value,
        help_text="请求类型"
    )

    class Meta:
        ordering = ['url', ]
        constraints = [
            models.UniqueConstraint(fields=['url', 'raw'], name='unique_request')
        ]

    @classmethod
    def from_request(cls, url_id, raw_id, request: RequestObject, request_type=RequestTypeEnum.NORMAL.value):
        return cls(
            url_id=url_id,
            raw_id=raw_id,
            method=request.method,
            request_headers=request.headers,
            request_body=request.content,
            request_type=request_type,
        )

    @property
    def request(self):
        return RequestObject(
            scheme=self.url.scheme,
            host=self.url.host,
            port=self.url.port,
            path=self.url.path,
            method=self.method,
            headers=self.request_headers,
            content=self.request_type,
        )


class Response(models.Model):

    RESPONSE_TYPE = tuple([
        (enum_item.value, enum_item.name)
        for enum_item in ResponseTypeEnum.__members__.values()
    ])

    url = models.ForeignKey("Url", editable=False, on_delete=models.CASCADE, related_name="response")
    raw = models.OneToOneField("Raw", on_delete=models.CASCADE, related_name="response")
    request = models.OneToOneField("Request", on_delete=models.CASCADE, related_name="response")

    status_code = models.IntegerField(editable=False, help_text="响应码")
    response_header = models.JSONField(editable=False, help_text="原始请求")
    response_body = models.BinaryField(max_length=5 * 1024, editable=False, help_text="响应 body")
    response_type = models.CharField(
        max_length=255,
        choices=RESPONSE_TYPE,
        default=ResponseTypeEnum.PlAIN.value,
        help_text="响应类型"
    )

    class Meta:
        ordering = ['url', ]
        constraints = [
            models.UniqueConstraint(fields=['url', 'raw'], name='unique_response')
        ]

    @classmethod
    def from_response(cls, url_id, raw_id, request_id, response: ResponseObject, response_type=ResponseTypeEnum.PlAIN.value):
        return cls(
            url_id=url_id,
            raw_id=raw_id,
            request_id=request_id,
            response_type=response_type,
            status_code=response.status_code,
            response_header=response.headers,
            response_body=response.content,
        )

    @property
    def response(self):
        return ResponseObject(
            status_code=self.status_code,
            headers=self.request_headers,
            content=self.request_type,
        )
