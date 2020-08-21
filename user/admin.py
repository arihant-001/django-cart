from django.contrib import admin
from user.models import CartUser


@admin.register(CartUser)
class CartUserAdmin(admin.ModelAdmin):
    pass
