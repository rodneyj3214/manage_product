from django.core.mail import EmailMultiAlternatives
from rest_framework import serializers

from manage_producs.products.models import Product
from manage_producs.users.models import User


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "name",
            "brand",
            "price",
        )

    def update(self, instance, validated_data):
        result = super().update(instance, validated_data)
        self.send_notification_email(instance)
        return result

    def send_notification_email(self, instance):
        email_list = []
        for user in User.objects.all():
            email_list.append(user.email)
        subject = f"Alert! this product was change {instance.name}"
        from_email = "from@example.com"
        text_content = "This message is for notify that this product was change."
        html_content = "This message is for notify that this product was change."
        msg = EmailMultiAlternatives(subject, text_content, from_email, email_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
