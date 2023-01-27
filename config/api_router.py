from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from manage_producs.products.api.views import ProductViewSet
from manage_producs.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("products", ProductViewSet)

app_name = "api"
urlpatterns = router.urls
