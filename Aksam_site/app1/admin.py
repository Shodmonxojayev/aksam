from django.contrib import admin

from .models import *

admin.site.register(Order),
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
