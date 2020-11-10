from django.contrib import admin
from .models import *
# Register your models here.


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Subscription._meta.get_fields()]


admin.site.register(Subscription, SubscriptionAdmin)


class SubTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'color']


admin.site.register(SubType, SubTypeAdmin)


class VideoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Video._meta.get_fields()]


admin.site.register(Video, VideoAdmin)


class TypeAccessAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TypeAccess._meta.get_fields()]


admin.site.register(TypeAccess, TypeAccessAdmin)


class TransationsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Transations._meta.get_fields()]


admin.site.register(Transations, TransationsAdmin)
