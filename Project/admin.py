from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.requestTable)
admin.site.register(models.classroom)
admin.site.register(models.labs)
admin.site.register(models.TimeTableEvents)