from django.contrib import admin
from accounts.models import Shopper

# Register your models here.
class AdminShopper(admin.ModelAdmin):
    list_display = ("username", "email", "number")
    
    
admin.site.register(Shopper, AdminShopper)

