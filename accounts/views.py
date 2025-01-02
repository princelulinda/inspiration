from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView, View
from banking_system import settings
from accounts.models import UserBankAccount, UserAddress, BankAccountType
from transactions import utils
from .forms import UserRegistrationForm, UserAddressForm, UserBankAccountForm
from django.shortcuts import get_object_or_404
import datetime

User = get_user_model()

def register_user(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(
                request,
                (
                    f'Merci de pouvoir créer un compte agent ! '
                    f'Votre nom d\'utilisateur est  {user.first_name}! '
                )
            )
        
        return redirect('accounts:accounts_user')
        
    
    context = {
        'form': form
    }
    return render(request, 'accounts/user_registration.html', context)


def get_accounts(request):
    accounts = UserBankAccount.objects.filter(user=request.user)
    
    context = {
        'accounts': accounts    
    }
    return render(request, 'accounts/accounts_user.html', context)

    
def details_bank_account(request, pk):
    accounts = UserBankAccount.objects.filter(user=request.user)
    account = accounts.get(account_no=pk)
    
    context = {
        'account': account,
        'title': f'DETAILS {pk}'
    }
    return render(request, 'accounts/details.html', context)   

class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:transaction_report')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        # address_form = UserAddressForm(self.request.POST)

        if registration_form.is_valid():
            #  and address_form.is_valid()
            user = registration_form.save()
            # address = address_form.save(commit=False)
            # address.user = user
            # address.save()
           

            login(self.request, user)
            messages.success(
                self.request,
                (
                    f'Thank You For Creating A Bank Account. '
                    f'Your Account Number is {user.account.account_no}. '
                )
            )
            return HttpResponseRedirect(
                reverse_lazy('transactions:deposit_money')
            )

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                # address_form=address_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        # if 'address_form' not in kwargs:
        #     kwargs['address_form'] = UserAddressForm()

        return super().get_context_data(**kwargs)

def bank_account_create(request):
    
    form = UserBankAccountForm()
   
    
    if request.method == "POST":
        form = UserBankAccountForm(request.POST)
        if form.is_valid():
            
            account_type = str(form.cleaned_data.get('account_type'))
            
            typeid = BankAccountType.objects.get(name=account_type)
            account_num = str(settings.ACCOUNT_NUMBER_START_FROM) + str(settings.randomGen()) + "INSP"
                
            account_bank = form.save(commit=False)
            account_bank.user = request.user
            account_bank.account_type = typeid
            
            account_bank.save()
            
            messages.success(
                    request,
                    (
                        f'Thank You For Creating A Bank Account. '
                        f'Your Account Number is {account_bank}. '
                    )
                )
                
                
            return HttpResponseRedirect(
                    reverse_lazy('accounts:account_view')
                )
             
    context = {
      'form' : form,
    }
    return render(request, 'accounts/account_create.html', context)

def bank_account_edit(request, account_no):
    # Get the existing bank account based on the provided account ID
    bank_account = get_object_or_404(UserBankAccount, account_no=account_no, user=request.user)
    
    # Initialize the form with the existing bank account data
    form = UserBankAccountForm(instance=bank_account)
    
    if request.method == "POST":
        form = UserBankAccountForm(request.POST, instance=bank_account)
        if form.is_valid():
            # Save the updated bank account details
            form.save()
            
            messages.success(
                request,
                f'Your Bank Account has been successfully updated.'
            )
            
            return HttpResponseRedirect(
                reverse_lazy('accounts:account_view')
            )
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/account_create.html', context)

class UserBankAccountView(LoginRequiredMixin, View):
    
    template_name = 'accounts/account_view.html'
    context = {
        "title" : "Comptes"
    }
    
    def post(self, request, *args, **kwargs):
        
        return render(request, self.template_name, self.context)
        
    def get(self, request, *args, **kwargs):
        accounts = UserBankAccount.objects.filter(user=request.user)
        items = utils.pagination(request, accounts)
        self.context['accounts'] = items
        
        
        return render(request, self.template_name, self.context)
            
class UserLoginView(LoginView):
    template_name='accounts/user_login.html'
    redirect_authenticated_user = False

class ProfileView(View):
    template_name = "accounts/profile.html"
    
    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)
    
    
class LogoutView(RedirectView):
    pattern_name = 'index'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)