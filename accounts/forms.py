from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User
from .models import User, BankAccountType, UserBankAccount, UserAddress
from .constants import GENDER_CHOICE

from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('entreprise', 'email', 'first_name', 'last_name')  # Les champs que vous voulez inclure
        exclude = ('password',)  # Les champs que vous voulez exclure

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        # Personnalisation supplémentaire ici
        self.fields['email'].widget.attrs['readonly'] = True  # Rendre le champ 'username' en lecture seule
    
class UserAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = [
            'street_address',
            'city',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
                )
            })


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 '
                    'rounded py-3 px-4 leading-tight '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                )
            })

class UserBankAccountForm(forms.ModelForm):
    account_type = forms.ModelChoiceField(
        queryset=BankAccountType.objects.all()
    )
   
    class Meta:
        model = UserBankAccount
        labels = {
            'name': "Nom",
            'first_name': "Nom de famille", 
            'email': "Addresse email (pas obligatoire)",
            'phone': "Numèro de téléphone", 
            'gender': "Genre", 
            'birth_date': "Date de naissance (JOUR/MOI/ANNEE)", 
            'street_address':"Addresse physique",
            
            
        }
        fields = ['name', 
                  'first_name', 
                  'email',
                  'phone', 
                  'gender', 
                  'birth_date', 
                  'street_address', 
                  'account_type',
             
                ]
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
                )
            })     