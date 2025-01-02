from django.urls import path
from . import views
urlpatterns = [
    path('credit', views.CreditView.as_view(), name='get_credit')
]