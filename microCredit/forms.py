from django import forms
from .models import Credit
from accounts.models import UserBankAccount

class CreditForm(forms.ModelForm):
    
    account = forms.ModelChoiceField(
        queryset=UserBankAccount.objects.all()
    )
    
    class Meta:
        model = Credit
        labels = {
            "amount": "Montant",
            "account": "Compte"
        }
        fields = [
            'amount',
            "account",
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
                )
            })