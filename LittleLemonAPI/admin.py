from django.contrib import admin
from .models import Category, MenuItem, Cart, Order, OrderItem

# Register your models here.
admin.site.register(MenuItem) # Registering 'MenuItem' model
admin.site.register(Category) # Registering 'Category' model
admin.site.register(Cart) # Registering 'Cart' model
admin.site.register(Order) # Registering 'Order' model
admin.site.register(OrderItem) # Registering 'OrderItem' model