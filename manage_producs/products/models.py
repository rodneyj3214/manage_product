from django.db import models


class Product(models.Model):
    name = models.CharField("Product Name", max_length=140)
    brand = models.CharField("Brand", max_length=255)
    price = models.FloatField("Price", default=0)

    def __str__(self):
        return self.name


class HistorySearchProduct(models.Model):
    ip_address = models.CharField("IP Address", max_length=140)
    creation_date = models.DateTimeField("Brand", auto_now_add=True)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)

    def __str__(self):
        return f"#{self.ip_address}: {self.product.name}"
