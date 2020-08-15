from django.db import models


from normal.constants import ValueTypeEnum, ParamPositionEnum, ParamTypeEnum

# Create your models here.


class Param(models.Model):

    VALUE_TYPE = tuple([
        (enum_item.value, enum_item.name)
        for enum_item in ValueTypeEnum.__members__.values()
    ])

    key = models.CharField(max_length=255, editable=False, help_text="键")
    value_type = models.CharField(choices=VALUE_TYPE, default=ValueTypeEnum.Unknown.value, max_length=255, editable=False, help_text="值类型")
    # {"values": []}
    values = models.JSONField()

    url = models.ForeignKey("raw.Url", on_delete=models.CASCADE, related_name="params")
    raw_param = models.ForeignKey("RawParam", on_delete=models.CASCADE, related_name="params")
    parnet = models.ForeignKey("Param", on_delete=models.CASCADE, related_name="children")

    class Meta:
        ordering = ['url', 'raw_param']
        indexes = [
            models.Index(
                fields=('url', '-raw_param'),
                name='websiteresult_ordering'
            )
        ]


class RawParam(models.Model):

    PARAM_POSITION = tuple([
        (enum_item.value, enum_item.name)
        for enum_item in ParamPositionEnum.__members__.values()
    ])
    PARAM_TYPE = tuple([
        (enum_item.value, enum_item.name)
        for enum_item in ParamTypeEnum.__members__.values()
    ])

    raw_param = models.BinaryField(max_length=5 * 1024, editable=False, help_text="原始参数")
    position = models.CharField(choices=PARAM_POSITION, default=ValueTypeEnum.Unknown.value, max_length=255, editable=False, help_text="参数位置")
    param_type = models.CharField(choices=PARAM_TYPE, default=ValueTypeEnum.Unknown.value, max_length=255, editable=False, help_text="参数类型")
    url = models.ForeignKey("raw.Url", on_delete=models.CASCADE, related_name="raw_parmas")

    class Meta:
        ordering = ['url', ]
