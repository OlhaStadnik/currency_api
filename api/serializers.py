from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserBalance, CurrencyExchange


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserBalance.objects.create(user=user)
        return user

class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBalance
        fields = ["user", "balance"]


class CurrencyExchangeSerializer(serializers.ModelSerializer):
    rate = serializers.ReadOnlyField()
    class Meta:
        model = CurrencyExchange
        fields = ["user", "currency_code", "rate", "created_at"]
