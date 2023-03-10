from django.urls import path

from apps.users.views import (
    UserDeleteView, UserRegistrationView, UserMeView,
    UserUpdateView, UserVerificationAccountView, UserVerificationView, UserReplenishmentBalanceView,
    UserWithdrawalBalanceView, UserCheckBalanceView
)

urlpatterns = [
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("me/", UserMeView.as_view(), name="user_me"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="user_patrial_update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),
    path("verification/", UserVerificationView.as_view(), name="user_verification"),
    path("verification/account/", UserVerificationAccountView.as_view(), name="user_account_verification"),
    path("add_balance/", UserReplenishmentBalanceView.as_view(), name='user_add_balance'),
    path("minus_balance/", UserWithdrawalBalanceView.as_view(), name='user_minus_balance'),
    path("check_balance/", UserCheckBalanceView.as_view(), name='user_check_balance'),
]
