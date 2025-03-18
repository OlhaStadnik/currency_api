import requests
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from rest_framework import status, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core import settings
from .models import UserBalance, CurrencyExchange
from .serializers import RegisterSerializer, UserBalanceSerializer, \
    CurrencyExchangeSerializer


class RegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


class BalanceView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserBalanceSerializer

    def list(self, request):
        user_balance = get_object_or_404(UserBalance, user=request.user)
        serializer = self.get_serializer(user_balance)
        return Response(serializer.data)


class CurrencyExchangeView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrencyExchangeSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        currency_code = request.data.get("currency_code")  # Отримуємо код валюти
        if not currency_code:
            return Response(
                {"error": "currency_code is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_balance = UserBalance.objects.get(user=user)
        if user_balance.balance <= 0:
            return Response(
                {"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST
            )

        api_key = settings.EXCHANGE_RATE_API_KEY
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency_code}"
        response = requests.get(url)
        print(response.status_code)

        if response.status_code != 200:
            return Response(
                {"error": "Failed to fetch exchange rate"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = response.json()
        rate = data.get("conversion_rates").get("UAH")

        if not rate:
            return Response(
                {"error": "Rate not found for UAH"}, status=status.HTTP_404_NOT_FOUND
            )

        # Створюємо запис в базі даних
        currency_exchange = CurrencyExchange.objects.create(
            user=user, currency_code=currency_code, rate=rate
        )

        serializer = self.get_serializer(currency_exchange)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HistoryView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrencyExchangeSerializer

    def get_queryset(self):

        user = self.request.user
        queryset = CurrencyExchange.objects.filter(user=user)

        currency_code = self.request.query_params.get("currency_code")
        if currency_code:
            queryset = queryset.filter(currency_code=currency_code)

        date = self.request.query_params.get("date")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if date:
            date = parse_date(date)
            queryset = queryset.filter(created_at__date=date.date())
        if start_date:
            queryset = queryset.filter(created_at__gte=parse_date(start_date))
        if end_date:
            queryset = queryset.filter(created_at__lte=parse_date(end_date))

        return queryset

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)