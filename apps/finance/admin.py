from django.contrib import admin
from .models import Subcategory, Account, Transaction

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'user')
    list_filter = ('type', 'user')
    search_fields = ('name', 'user__username')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'user')
    list_filter = ('subcategory__type', 'user')
    search_fields = ('name', 'subcategory__name', 'user__username')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'account', 'value', 'status', 'user')
    list_filter = ('status', 'account__subcategory__type', 'date', 'user')
    search_fields = ('description', 'account__name', 'user__username')
    date_hierarchy = 'date'
