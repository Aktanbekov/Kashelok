from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.users.models import User
from decimal import Decimal
from django.db import transaction


class UserReplenishmentBalanceMixin:
    @transaction.atomic
    def get(self, request):
        phone_number = request.GET.get("phone_number")
        if not phone_number:
            raise ValueError("Not phone number")

        amount = request.GET.get("amount")
        if not amount:
            raise ValueError("Not amount number")

        user = get_object_or_404(User, phone_number=phone_number)
        user.balance += Decimal(amount)
        user.save()
        return Response(data={"msg": "Ok"}, status=201)


class UserWithdrawalBalanceMixin:
    @transaction.atomic
    def get(self, request):
        phone_number = request.GET.get("phone_number")
        if not phone_number:
            raise ValueError("Not phone number")

        amount = request.GET.get("amount")
        if not amount:
            raise ValueError("Not amount number")

        user = get_object_or_404(User, phone_number=phone_number)
        user.balance -= Decimal(amount)
        user.save()
        return Response(data={"msg": "Ok"}, status=201)


class UserVerificationAccountMixin:
    def retrieve(self, request, *args, **kwargs):
        phone_number = request.GET.get("phone_number")
        user = get_object_or_404(User, phone_number=phone_number)
        return Response({"mgs": "OK"})


class UserMeMixin:
    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id).first()
        serializer = self.get_serializer_class()(user)
        return Response(status=200, data=serializer.data)
