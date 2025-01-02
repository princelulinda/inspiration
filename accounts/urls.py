from django.urls import path

from .views import (
    ProfileView, register_user, get_accounts,LogoutView, UserLoginView, UserBankAccountView, bank_account_create, details_bank_account,
    bank_account_edit
)


app_name = 'accounts'

urlpatterns = [
    path(
        "login/", UserLoginView.as_view(),
        name="user_login"
    ),
    path(
        "logout/", LogoutView.as_view(),
        name="user_logout"
    ),
    path(
        "register/", register_user,
        name="user_registration"
    ),
    path('accounts-report/', get_accounts, name='accounts_user'),
    path('account-bank-create/', bank_account_create, name='create_abank_account'),
    path('account-details/<str:pk>', details_bank_account, name='details'),
    path('account-edit/<str:account_no>', bank_account_edit, name='account_edit'),

    path('profile', ProfileView.as_view(), name="profile"),
    path("account-view/", UserBankAccountView.as_view(), name="account_view")
]
