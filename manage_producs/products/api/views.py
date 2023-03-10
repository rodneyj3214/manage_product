from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from manage_producs.products.api.serializers import ProductModelSerializer
from manage_producs.products.models import HistorySearchProduct, Product

User = get_user_model()


class ProductViewSet(ModelViewSet):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()

    def get_permissions(self):
        """Change permissions for the list can access for all requests"""
        if self.action in ["list"]:
            permissions = [AllowAny]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        for element in queryset:
            # Create Record for the product and anonymous request
            new = HistorySearchProduct(
                product=element, ip_address=request.META["REMOTE_ADDR"]
            )
            new.save()
        return Response(serializer.data)
