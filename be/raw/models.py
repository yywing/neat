from django.db import models

from raw.constants import SchemaEnum, RequestMethodEnum, RequestTypeEnum, ResponseTypeEnum
# Create your models here.


class Raw(models.Model):
    raw_request = models.BinaryField(max_length=5 * 1024, editable=False, help_text="原始请求")
    raw_response = models.BinaryField(max_length=1024 * 1024, null=True, blank=False, editable=False, help_text="原始响应")
    created_time = models.DateTimeField(auto_now_add=True)

    url = models.ForeignKey("Url", on_delete=models.CASCADE, related_name="raws")

    class Meta:
        ordering = ['-created_time', ]


class Url(models.Model):

    SCHEMA = tuple([
        (enum_item.value, enum_item.name)
        for enum_item in SchemaEnum.__members__.values()
    ])

    schema = models.CharField(choices=SCHEMA, max_length=255, editable=False)
    host = models.CharField(max_length=255, editable=False)
    path = models.CharField(max_length=255, editable=False)
    url = models.CharField(max_length=255, editable=False)
    suffix = models.CharField(max_length=255, editable=False)

    class Meta:
        ordering = ['url', ]


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
    request_header = models.JSONField(editable=False, help_text="原始请求")
    request_body = models.BinaryField(max_length=5 * 1024, editable=False, help_text="请求 body")
    request_type = models.CharField(
        max_length=255,
        choices=REQUEST_TYPE,
        default=RequestTypeEnum.NOEMAL.value,
        help_text="请求类型"
    )

    class Meta:
        ordering = ['url', ]


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
