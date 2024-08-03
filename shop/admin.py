from django.contrib import admin

# Register your models here.
from .models import Product, Contact, Orders, OrderUpdate, SingleOrders, SingleOrderUpdate, Customer

#admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
        list_display = ('product_name','category','price','desc','image_tag')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ('name','email','phone','desc','msg_id')

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
	list_display = ('order_id','amount','address','city','state','timestamp')

@admin.register(OrderUpdate)
class OrderUpdateAdmin(admin.ModelAdmin):
	list_display = ('update_id','order_id','update_desc','timestamp')

@admin.register(SingleOrders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id1','pname','quant','pprice','address','city','state','timestamp')

@admin.register(SingleOrderUpdate)
class SingleOrderUpdateAdmin(admin.ModelAdmin):
	list_display = ('order_id1','update_desc','timestamp')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ('id','user','name','email','locality','city','state', 'zipcode')
