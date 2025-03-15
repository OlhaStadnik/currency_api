from django.db import models
from django.contrib.auth import get_user_model



User = get_user_model()


class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="balance")
    balance = models.IntegerField(default=1000)

    def __str__(self):
        return f"{self.user} - Balance: {self.balance}"


class CurrencyExchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exchanges")
    currency_code = models.CharField(max_length=10)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} exchanged {self.currency_code} at {self.rate}"

