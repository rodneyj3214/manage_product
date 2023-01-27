from rest_framework import serializers

from manage_producs.products.models import Product


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "name",
            "brand",
            "price",
        )
