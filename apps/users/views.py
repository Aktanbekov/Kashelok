from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework import permissions

from apps.users.models import User
from apps.users.serializers import (
    UserMeSerializer, UserRegistrationSerializer, UserVerificationSerializer, VerifyUserAccountSerializer, UserCheckBalanceSerializer
)

from apps.users.mixins import (
    UserReplenishmentBalanceMixin, UserVerificationAccountMixin, UserWithdrawalBalanceMixin, UserMeMixin
)


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)


class UserMeView(UserMeMixin, ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserMeSerializer
    permission_classes = (permissions.AllowAny,)


class UserUpdateView(UpdateAPIView, RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserMeSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserMeSerializer


class UserVerificationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserVerificationSerializer


class UserVerificationAccountView(UserVerificationAccountMixin, RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = VerifyUserAccountSerializer


class UserReplenishmentBalanceView(UserReplenishmentBalanceMixin, APIView):
    pass


class UserWithdrawalBalanceView(UserWithdrawalBalanceMixin, APIView):
    pass


class UserCheckBalanceView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserCheckBalanceSerializer  

    def get_object(self):
        return self.request.user
