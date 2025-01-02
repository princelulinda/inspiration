from django.db import models
from accounts.models import UserBankAccount, User
import decimal
# Create your models here.


class Credit(models.Model):
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=0
    )
    
    
    user = models.ForeignKey(User, related_name="user_creation", on_delete=models.CASCADE)
    
    account = models.ForeignKey(UserBankAccount, on_delete=models.CASCADE, related_name="credits")
    
    trans_type = models.CharField(max_length=50, null=True, blank=True)
    
    is_paid = models.BooleanField(default=False)
    
    returned_at = models.DateField(auto_now=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        
        return f"_{self.account}"
    
    @property
    def estimeted(self):
        taux_interet = 10 / 100
        total = self.amount * round(decimal.Decimal((1 + taux_interet)), 2)
        
        return total
    
class HistoryMicroCredit(models.Model):
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    
    history_acc = models.ForeignKey(UserBankAccount, on_delete=models.CASCADE, related_name='histories')
    trans_type = models.CharField(max_length=50)
    is_paid = models.BooleanField(default=False)
    returned_at = models.DateField(null=False)
    added_at = models.DateTimeField(auto_now_add=True)