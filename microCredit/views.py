from django.shortcuts import render, redirect

from common.decorators import LoginRequiredStaffMixim
from .forms import CreditForm
from .models import Credit
from django.contrib import messages
from django.views import View
from accounts.models import UserBankAccount
from decimal import Decimal
# Create your views here.


class CreditView(LoginRequiredStaffMixim, View):
    form = CreditForm()
    
    context = {
            'form': form,
            "title": "Donnez un emprunt",
        }
    
    def get(self, request, *args, **kwargs):
        creditss = Credit.objects.filter(is_paid=False).order_by('added_at')
        self.context['creditss'] = creditss
        
        return render(request, 'credit/get_credit.html', self.context)
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == "credit":
            try:
                form = CreditForm(request.POST)
                if form.is_valid():
                    
                    credit = form.save(commit=False)
                    credit.user = request.user
                    
                    credit.save()
                    montant_gain = credit.estimeted - credit.amount
                    entreprise = request.user.entreprise
                    entreprise.gain_surcerdit += montant_gain
                    entreprise.save()
                    
                    accounts = UserBankAccount.objects.get(account_no=credit.account.account_no)
                    accounts.credit = credit.estimeted
                    accounts.save()
                    messages.success(request, "Enregistrement avec succes")
                    return redirect('get_credit')
                
                
            except Exception as e:
                print(e)
                
                messages.error(request, "Echec !")
            
        if request.POST.get("action") == "rembourser":
            id_modified = request.POST.get("ismodified")
            if id_modified:
                credit = Credit.objects.get(id=id_modified)
                isPaid = request.POST.get('isPaid')
                account = UserBankAccount.objects.get(account_no=credit.account.account_no)
                if isPaid == "True":
                    credit.is_paid = True
                    account.credit = 0
                if isPaid == "avance":
                    montant_ = Decimal(request.POST.get("montant"))
                    if montant_:
                        remaind_deb = account.credit - montant_
                        if remaind_deb <= 0:
                            credit.is_paid = True
                        
                        account.credit -= montant_
                        
                account.save()
                credit.save()
                
                messages.success(request, "Modification emprunt effectué avec succes")
                return redirect('get_credit')
                            
        return render(request, 'credit/get_credit.html', self.context)