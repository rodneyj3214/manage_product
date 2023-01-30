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
        """Custom process for after update model"""
        result = super().update(instance, validated_data)
        # Send notification on update Product
        self.send_notification_email(instance)
        return result

    def send_notification_email(self, instance):
        """Send Email notification for all users with tha product info"""
        email_list = User.objects.values_list("email", flat=True)
        subject = f"Alert! this product was change {instance.name}"
        from_email = "from@example.com"
        text_content = "This message is for notify that this product was change."
        html_content = "This message is for notify that this product was change."
        msg = EmailMultiAlternatives(subject, text_content, from_email, email_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
