from django.contrib import admin
from .models import UserBalance, CurrencyExchange

admin.site.register(UserBalance)
admin.site.register(CurrencyExchange)
