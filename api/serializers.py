from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserBalance


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserBalance.objects.create(user=user)  # Створюємо баланс 1000 монет
        return user
