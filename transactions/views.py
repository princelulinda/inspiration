import decimal
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from banking_system import settings
from django.utils import timezone
from django.views.generic import CreateView, View
from accounts.models import User, UserBankAccount
from django.db import transaction

from common.decorators import LoginRequiredStaffMixim
from .utils import pagination
from .constants import DEPOSIT, WITHDRAWAL
from .forms import (
    DepositForm,
    TransactionDateRangeForm,
    WithdrawForm, TransactionDateRangeForm
)
from .models import Transaction, TransactionCaisse, WithdrawlGainHistorique

cur_customer_num = int

# def display_subaccount(request):
#     global cur_customer
    
#     cur_customer = SubAccount.objects.filter(accounts=request.user.account)
    
#     return cur_customer
# display_subaccount(cur_customer)
class TransactionRepostView(LoginRequiredMixin, View):
    context = {
        'title': "Transactions",
        'form': TransactionDateRangeForm()
    }
    
    form_data = {}
    
    template_name = 'transactions/transaction_report.html'
    
    
    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(user=request.user)
        items = pagination(request, transactions)
        total_retrait = sum(item.amount for item in Transaction.objects.filter(transaction_type=WITHDRAWAL))
        total_deposit = sum(item.amount for item in Transaction.objects.filter(transaction_type=DEPOSIT))
        self.context['transactions'] = items
        self.context['total_retrait'] = total_retrait
        self.context['total_deposit'] = total_deposit
        
        
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        if request.POST.get("action") == "search":
            account  = request.POST.get("account")
            startdate = request.POST.get("start")
            enddate = request.POST.get("end")
            items = {}
            if account:
                items = Transaction.objects.filter(account__account_no=account)
            
            if startdate or enddate:
                items = Transaction.objects.filter(timestamp__range=[startdate, enddate])

            try:
                transactions = pagination(request, items)
                total_retrait = sum(item.amount for item in items.filter(transaction_type=WITHDRAWAL))
                total_deposit = sum(item.amount for item in items.filter(transaction_type=DEPOSIT))
                self.context['transactions'] = transactions
                self.context['total_retrait'] = total_retrait
                self.context['total_deposit'] = total_deposit
            except:
                pass
            
            return render(request, self.template_name, self.context)
                
        
        return render(request, self.template_name, self.context)
    
class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    p = ''
    message = ''
    success_url = reverse_lazy('transactions:transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'p': self.p,
        })

        return context


class DepositMoneyView(LoginRequiredMixin, View):
    template_name = 'transactions/deposit.html'

    title = 'DEPOT D\'ARGENT'
    p = f'Déposer votre argent en mettant le numero de compte dont vous souhaitez nourrir \n minimum depôt {settings.MINIMUM_WITHDRAWAL_AMOUNT}'
    
    context = {
        'title': title,
        'p': p
    }
    
    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        transaction_type = request.POST.get("transaction_type")
        amount = decimal.Decimal(request.POST.get("amount"))
        account_num = request.POST.get("account_num")
        print(account_num)
        with transaction.atomic():
            
            try:
                account = UserBankAccount.objects.get(account_no=account_num)
                balance_after_transaction = account.balance
                if account:
                    transactions = Transaction.objects.create(
                        balance_after_transaction = balance_after_transaction,
                        transaction_type=DEPOSIT,
                        amount=amount,
                        account = account,
                        user = request.user
                    )
            
                    transactions.save()
                    if amount > 0:
                        transactions.status = Transaction.APPROVED
                        
                        account.balance += amount
                        account.save()
                        transactions.save()
                        messages.success(request, "Transaction reussi")
                        return redirect("transactions:transaction_report")
                    else:
                        transactions.status = Transaction.DENIED
                        transactions.save()
                        messages.error(request, "Transaction refusée")
                else:
                    messages.error(request, "Ce compte n'existe pas, veuillez entrer un compte valide")
                    return redirect("transactions:deposit_money")
                
                messages.success("Oui numero existe")
            except Exception as e:
                print(e)
                messages.error(request, "Quelque chose s'est mal passée, veuillez entrer un compte valide et réessayer encore")
        
        
        return render(request, self.template_name, self.context)

class WithdrawMoneyView(LoginRequiredStaffMixim, View):
    template_name = 'transactions/withdrawl.html'
    title = 'RETRAIT D\'ARGENT'
    p = f'Rétirer votre argent en mettant le numero de compte dont vous souhaitez \n minimum de retrait {settings.MINIMUM_WITHDRAWAL_AMOUNT}'

    context = {
        'title': title,
        'p': p
    }
    
    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        transaction_type = request.POST.get("transaction_type")
        amount = decimal.Decimal(request.POST.get("amount"))
        account_num = request.POST.get("account_num")
        mise = decimal.Decimal(request.POST.get("mise"))
        with transaction.atomic():
            try:
                account = UserBankAccount.objects.get(account_no=account_num)
                balance_after_transaction = account.balance
                if account:
                    transactions = Transaction.objects.create(
                        account = account,
                        user = request.user,
                        mise=mise,
                        amount=amount,
                        balance_after_transaction = balance_after_transaction,
                        transaction_type=WITHDRAWAL
                    )
                    transactions.save()
                    if account.balance >= (amount + mise):
                        transactions.status = Transaction.APPROVED
                        balance = request.user.entreprise
                        montant_user = mise / 2
                        balance.balance += montant_user
                        balance.save()
                        account.balance -= (amount + mise)
                        user_balance = User.objects.get(id=account.user.id)
                        user_balance.balance += montant_user
                        user_balance.save()
                        account.save()
                        transactions.save()
                        messages.success(request, "Transaction reussi")
                        return redirect("transactions:transaction_report")
                    else:
                        transactions.status = Transaction.DENIED
                        transactions.save()
                        messages.error(request, "Solde insufisant")
                        return redirect("transactions:withdraw_money")
                          
                messages.success("Oui numero existe")
            except Exception as e:
                print(e)
                messages.error(request, "Quelque chose s'est mal passée, veuillez réessayer encore")
        
        return render(request, self.template_name, self.context)
    
class TransactionCaisseView(LoginRequiredStaffMixim, View):
    template_name = 'transactions/caisse_withdrawal.html'
    transactions = TransactionCaisse.objects.all().order_by("timestamp")
    
    context = {
        "title": "Paiement caisse, agents",
    }
    
    def get(self, request, *args, **kwargs):
        transactions = TransactionCaisse.objects.all().order_by("timestamp")
        items = pagination(request, transactions)
        transactions_cas = WithdrawlGainHistorique.objects.all().order_by("timestamp")
        itemses = pagination(request, transactions_cas)
        self.context['transactions'] = items
        self.context['transactions_cas'] = itemses
        
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        if request.POST.get("action") == "retrait_agent":
            user_agent_email = request.POST.get("user_agent_email")
            amount = decimal.Decimal(request.POST.get("amount"))
            motif = request.POST.get("motif")
            
            try:
                user = User.objects.get(email=user_agent_email)
            except User.DoesNotExist as e:
                print(e)
                messages.error(request, f"Error: {e}")
                
                return redirect("transactions:paiements")
            
            user = User.objects.get(email=user_agent_email)
            
            if user.balance > amount:
                caisse_transa = TransactionCaisse.objects.create(
                    from_account_user_email=user.email,
                    saved_by=request.user,
                    amount = amount,
                    transaction_type=WITHDRAWAL,
                    status=TransactionCaisse.APPROVED,
                    motif=motif
                )
                caisse_transa.save()
                
                user.balance -= amount
                user.save()
                messages.success(request, "Paiement effectué")
            else:
                caisse_transa = TransactionCaisse.objects.create(
                    from_account_user_email=user.email,
                    saved_by=request.user,
                    amount = amount,
                    transaction_type=WITHDRAWAL,
                    status=TransactionCaisse.DENIED,
                    motif=motif
                )
                caisse_transa.save()
                messages.error(request, "Le montant associé à cet email est insufisant")
                
        if request.POST.get("action") == "gains":
            amount = decimal.Decimal(request.POST.get("amount_"))
            motif = request.POST.get("motif_")
            entreprise = request.user.entreprise
            
            if entreprise.balance > amount:
                eithdre = WithdrawlGainHistorique.objects.create(
                    motif=motif,
                    saved_by = request.user,
                    transaction_type=WITHDRAWAL,
                    status=WithdrawlGainHistorique.APPROVED,
                    amount=amount
                )
                eithdre.save()
                entreprise.balance -= amount
                entreprise.save()
                
                messages.success(request, "Transaction reussie !")
                
                return redirect("transactions:paiements")
            else:
                if entreprise.gain_surcerdit > amount:
                    eithdre = WithdrawlGainHistorique.objects.create(
                        motif=motif,
                        saved_by = request.user,
                        transaction_type=WITHDRAWAL,
                        status=WithdrawlGainHistorique.APPROVED,
                        amount=amount
                    )
                    eithdre.save()
                    entreprise.gain_surcerdit -= amount
                    entreprise.save()
                    
                    messages.success(request, "Transaction reussie !")
                    
                    return redirect("transactions:paiements")
                
            messages.error(request, "Une erreur est survenue lors de la verification de la requete.")

        return render(request, self.template_name, self.context)
    
    