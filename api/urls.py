from rest_framework import routers
from .views import RegisterView, BalanceView

router = routers.DefaultRouter()
router.register("register", RegisterView, basename="register")
router.register("balance", BalanceView, basename="balance")

urlpatterns = router.urls


app_name = "api"