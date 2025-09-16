from django.contrib import admin
from .models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User

#Register model on Admin panel
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#create an OrderItem inline
class OrderItemInline(admin.StackedInline):
    model=OrderItem
    #we dont want extra order items
    extra=0

#extend our Order Model
class OrderAdmin(admin.ModelAdmin):
    model=Order
    readonly_fields=["date_ordered"]
    fields=["user","full_name","email","shipping_address","amount_paid","date_ordered","shipped","date_shipped"]
    inlines=[OrderItemInline] 

#First unregister order model
admin.site.unregister(Order)

#Re-register Order and OrderItems Model
admin.site.register(Order,OrderAdmin)

