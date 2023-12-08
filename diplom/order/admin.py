from django.contrib import admin

from .models import Order, Notification, Order_a_call

admin.site.register(Order)
admin.site.register(Notification)
admin.site.register(Order_a_call)


