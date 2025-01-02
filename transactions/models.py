from django.db import models
from django.utils.translation import gettext_lazy as _
from .constants import TRANSACTION_TYPE_CHOICES
from accounts.models import UserBankAccount, User


class Transaction(models.Model):
    APPROVED = 'approved'
    PENDING = 'pending'
    DENIED = 'denied'
    EXPIRED = 'expired'
    
    TRANSACTION_STATUS = (
        (APPROVED, 'Approved'),
        (PENDING, 'Pending'),
        (DENIED, 'Denied'),
        (EXPIRED, 'Expired')
    )
    
    account = models.ForeignKey(
        UserBankAccount,
        related_name='transaction',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,blank = True, null=True
    )
    balance_after_transaction = models.DecimalField(
        decimal_places=2,
        max_digits=12, blank = True, null=True
    )
    
    mise = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        blank = True, null=True
    )
    
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE_CHOICES,
        max_length=50, blank = True, null=True
    )
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(
        verbose_name=_("Ordered Status"),
        choices=TRANSACTION_STATUS,
        default=PENDING,
        blank = True, null=True,
        help_text=_('The ordered Status of the client'),
        max_length=15
    )

    def __str__(self):
        return str(self.account.account_no)

    class Meta:
        ordering = ['timestamp']



class TransactionCaisse(models.Model):
    APPROVED = 'approved'
    PENDING = 'pending'
    DENIED = 'denied'
    EXPIRED = 'expired'
    
    TRANSACTION_STATUS = (
        (APPROVED, 'Approved'),
        (PENDING, 'Pending'),
        (DENIED, 'Denied'),
        (EXPIRED, 'Expired')
    )
    
    from_account_user_email = models.EmailField()
    saved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,blank = True, null=True
    )
    balance_after_transaction = models.DecimalField(
        decimal_places=2,
        max_digits=12, blank = True, null=True
    )
    
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE_CHOICES,
        max_length=50, blank = True, null=True
    )
    
    motif = models.CharField(max_length=250, blank = True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(
        verbose_name=_("Ordered Status"),
        choices=TRANSACTION_STATUS,
        default=PENDING,
        blank = True, null=True,
        help_text=_('The ordered Status of the client'),
        max_length=15
    )

    def __str__(self):
        return str(self.from_account_user_email)

    class Meta:
        ordering = ['timestamp']

class WithdrawlGainHistorique(models.Model):
    APPROVED = 'approved'
    PENDING = 'pending'
    DENIED = 'denied'
    EXPIRED = 'expired'
    
    TRANSACTION_STATUS = (
        (APPROVED, 'Approved'),
        (PENDING, 'Pending'),
        (DENIED, 'Denied'),
        (EXPIRED, 'Expired')
    )
     
    
    saved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,blank = True, null=True
    )
    
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE_CHOICES,
        max_length=50, blank = True, null=True
    )
    
    motif = models.CharField(max_length=250, blank = True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(
        verbose_name=_("Ordered Status"),
        choices=TRANSACTION_STATUS,
        default=PENDING,
        blank = True, null=True,
        help_text=_('The ordered Status of the client'),
        max_length=15
    )
    
    def __str__(self):
        
        return f'{self.saved_by},,, {self.timestamp}'