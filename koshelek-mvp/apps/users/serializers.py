import random
from rest_framework import serializers

from apps.users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "phone_number", "password")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data, code=str(random.randint(1000, 9999)))
        user.set_password(password)
        user.save()
        return user


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "phone_number", "last_name", "first_name", "surname", "username", "email")
        read_only_fields = ("id",)


class UserVerificationSerializer(serializers.ModelSerializer):
    unique_code = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "is_active", "unique_code", 'phone_number')
        read_only_fields = ("is_active",)

    def create(self, validated_data):
        user = User.objects.filter(phone_number=validated_data.get('phone_number')).first()
        if not user:
            raise serializers.ValidationError({"Message": "User is not found"})
        if user.is_active:
            raise serializers.ValidationError({"Message": "User alredy is active"})
        if user.code == validated_data.get("unique_code"):
            user.is_active = True
        user.save()
        return user


class VerifyUserAccountSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("phone_number",)


class UserCheckBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "balance", )  
