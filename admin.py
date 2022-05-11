from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Group)
admin.site.register(GroupFile)


@admin.register(File)
class RateAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "date", "type")
    list_filter = ("user", "type")
    search_fields = ("description",)
