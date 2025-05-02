from email import message
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, ShippingAdress

@shared_task
def send_order_confirmation(order_id):
    order = Order.objects.get(id=order_id)
    subject = f" Order Confirmation #{order_id}"
    receipent_data = ShippingAdress.objects.get(user=order.user)
    receipent_email = receipent_data.email

    message=f"Hello your order and payment has been completed successfully. Order ID: {order_id}."

    mail_to_sender = send_mail(subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[receipent_email])

    return mail_to_sender