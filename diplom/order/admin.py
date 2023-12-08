from django.contrib import admin

from .models import Order, Notification

admin.site.register(Order)
admin.site.register(Notification)

