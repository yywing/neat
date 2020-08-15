from django.contrib import admin

from raw.models import Raw, Url, Request, Response
# Register your models here.


admin.site.register(Raw)
admin.site.register(Url)
admin.site.register(Request)
admin.site.register(Response)
