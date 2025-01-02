from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import BankAccountType, User, Entreprise, UserBankAccount
from .forms import CustomUserChangeForm

class AdminUserBankAccount(admin.ModelAdmin):
    list_display = ['account_no', 'name', 'first_name', 'phone', 'email', 'balance', 'account_type', 'credit']
    search_fields = ['account_no', 'name']
    
class AdminBankAccountType(admin.ModelAdmin):
    list_display = ['id', 'name', 'maximum_withdrawal_amount', 'annual_interest_rate', 'interest_calculation_per_year']
    search_fields = ['name']

class AdminSubAccount(admin.ModelAdmin):
    list_display = ['subaccount_no', 'motif', 'balance', 'is_active', 'added_at']
    search_fields = ['subaccount_no']


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_staff', 'is_superuser','is_active','first_name', 'last_name', 'entreprise',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'entreprise',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser','entreprise', 'first_name', 'last_name')}
        ),
    )
    
    search_fields = ('email','first_name', 'last_name')
    ordering = ('email',)

admin.site.register(BankAccountType, AdminBankAccountType)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Entreprise)
admin.site.register(UserBankAccount, AdminUserBankAccount)