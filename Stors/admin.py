from django.contrib import admin
from Stors.models import Cart, Contact, GroupeProduct, Order, Product


# Register your models here.
admin.site.register(Product)
admin.site.register(GroupeProduct)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(Cart)
