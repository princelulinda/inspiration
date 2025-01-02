from django.contrib import admin
from .models import Credit
# Register your models here.

class AdminCredit(admin.ModelAdmin):
    list_display = ['id', 'amount', 'account', 'is_paid', 'added_at']
    search_fields = ['added_at']
    
admin.site.register(Credit, AdminCredit)