from rest_framework import routers
from .views import RegisterView, BalanceView, CurrencyExchangeView, HistoryView

router = routers.DefaultRouter()
router.register("register", RegisterView, basename="register")
router.register("balance", BalanceView, basename="balance")
router.register("exchange", CurrencyExchangeView, basename="exchange")
router.register("history", HistoryView, basename="history")
urlpatterns = router.urls


app_name = "api"