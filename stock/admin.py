from django.contrib import admin
from stock.models import Shop, User, Product, Stock, Synchronisation

class UserAdmin(admin.ModelAdmin):
    model = User

# Register your models here.
admin.site.register(User, UserAdmin)