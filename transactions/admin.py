from django.contrib import admin

from transactions.models import Transaction, TransactionCaisse, WithdrawlGainHistorique
class AdminTransaction(admin.ModelAdmin):
    list_display = ['id', 'amount', 'account', 'user', 'transaction_type', 'timestamp', 'status', 'timestamp']
    search_fields = ['timestamp']
    
admin.site.register(Transaction, AdminTransaction)
admin.site.register(TransactionCaisse)
admin.site.register(WithdrawlGainHistorique)
