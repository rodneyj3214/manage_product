from django.db import models


class Product(models.Model):
    name = models.CharField("Product Name", max_length=140)
    brand = models.CharField("Brand", max_length=255)
    price = models.FloatField("Price", default=0)

    # picture = models.ImageField(upload_to="products/pictures", blank=True, null=True)

    def __str__(self):
        return self.name
