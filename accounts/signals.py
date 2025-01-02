from django.db.models.signals import pre_save
from .models import UserBankAccount
from django.dispatch import receiver
from django.utils.text import slugify

@receiver(pre_save, sender=UserBankAccount)
def generate_account_no(sender, instance, *args, **kwargs):
    
    if not instance.account_no:
        last_user = UserBankAccount.objects.order_by("-id").first()
        
        if last_user:
            last_id = last_user.id
        else:
            last_id = 0
        
        instance.account_no = f"INSP{str(last_id + 1).zfill(4)}"