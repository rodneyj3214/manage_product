from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from manage_producs.products.api.serializers import ProductModelSerializer
from manage_producs.products.models import Product

User = get_user_model()


class ProductViewSet(ModelViewSet):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()

    def get_permissions(self):
        if self.action in ["list"]:
            permissions = [AllowAny]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response
