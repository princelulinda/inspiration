from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import UserBankAccount, User
from blogue.models import Article, Tag
from transactions import utils, models, constants

class HomeViewIndex(View):
    template_name = 'core/home.html'
    articles = Article.objects.all()[:10]
    tags = Tag.objects.all()
    
    context = {
        'title': "Home vie",
        'articles': articles,
        'tags': tags
    }
    
    def get(self, request,*args, **kwargs):
        
        return render(request, self.template_name, self.context)

class HomeView(View):
    template_name = 'index.html'
    
    context = {
        'title': "Tableau de bord"
    }
    
    def get(self, request,*args, **kwargs):
        
        print(self.context)

        return render(request, self.template_name, self.context)
    
    
class DashboardView(LoginRequiredMixin, View):
    template_name = 'core/dashboard.html'
    
    context = {
        'title': "Tableau de bord"
    }
    
    def get(self, request,*args, **kwargs):
        accounts = UserBankAccount.objects.filter(user=request.user)
        items = utils.pagination(request, accounts)
        totalclients = UserBankAccount.objects.all()
        transactions = models.Transaction.objects.all()
        
        self.context['accounts'] = items
        self.context['totalclients'] = totalclients.count
        self.context['transactions_solde_deposit'] = sum(item.amount for item in transactions.filter(transaction_type=constants.DEPOSIT))
        self.context['transactions_solde_retrailt'] = sum(item.amount for item in transactions.filter(transaction_type=constants.WITHDRAWAL))
        self.context['solde'] = sum(item.balance for item in totalclients)
        self.context['totalmembres'] = User.objects.all().count
        
        return render(request, self.template_name, self.context)    

