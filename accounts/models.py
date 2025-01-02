from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models

from .constants import GENDER_CHOICE
from .managers import UserManager

class Entreprise(models.Model): 
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gain_surcerdit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    logo = models.FileField(blank=True, null=True, upload_to='logo')
    cretead_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    entreprise = models.ForeignKey(Entreprise, related_name="entreprise", on_delete=models.CASCADE, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    # @property
    # def balance(self):
    #     if hasattr(self, 'account'):
    #         return self.account.balance
    #     return 0


class BankAccountType(models.Model):
    name = models.CharField(max_length=128)
    maximum_withdrawal_amount = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    mise = models.DecimalField(max_digits=10, 
                               decimal_places=2, default=0,
                               help_text="La mise qui sera effectué par chaque transaction",
                               verbose_name="",
                               )
    carnet = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    annual_interest_rate = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        decimal_places=2,
        max_digits=5,
        help_text='Interest rate from 0 - 100'
    )
    interest_calculation_per_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text='The number of times interest will be calculated per year'
    )

    def __str__(self):
        return self.name

    def calculate_interest(self, principal):
        """
        Calculate interest for each account type.

        This uses a basic interest calculation formula
        """
        p = principal
        r = self.annual_interest_rate
        n = Decimal(self.interest_calculation_per_year)

        # Basic Future Value formula to calculate interest
        interest = (p * (1 + ((r/100) / n))) - p

        return round(interest, 2)


class UserBankAccount(models.Model):
    user = models.ForeignKey(
        User,
        related_name='account',
        on_delete=models.CASCADE,
    )
    account_type = models.ForeignKey(
        BankAccountType,
        related_name='accounts',
        on_delete=models.CASCADE
    )
    account_no = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    birth_date = models.DateField(null=True, blank=True)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    mise = models.DecimalField(max_digits=10, 
                               decimal_places=2, default=0,
                               help_text="La mise qui sera effectué par chaque transaction",
                               )
    carnet = models.DecimalField(max_digits=10, decimal_places=2, default=500, editable=False)
    
    street_address = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    
    interest_start_date = models.DateField(
        null=True, blank=True,
        help_text=(
            'The month number that interest calculation will start from'
        )
    )
    initial_deposit_date = models.DateField(null=True, blank=True)

    def __str__(self):
        
        return f"=>{self.account_no} {self.first_name} {self.name}"

    def get_interest_calculation_months(self):
        """
        List of month numbers for which the interest will be calculated

        returns [2, 4, 6, 8, 10, 12] for every 2 months interval
        """
        interval = int(
            12 / self.account_type.interest_calculation_per_year
        )
        start = self.interest_start_date.month
        return [i for i in range(start, 13, interval)]


class UserAddress(models.Model):
    account_bank = models.OneToOneField(
        UserBankAccount,
        related_name='address',
        on_delete=models.CASCADE,
    )
    street_address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)

    def __str__(self):
        return self.account_bank.name