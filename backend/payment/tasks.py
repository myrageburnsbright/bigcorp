from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, ShippingAdress
from django.contrib.auth import get_user_model
User = get_user_model()

@shared_task
def send_order_confirmation(order_id):
    order = Order.objects.get(id=order_id)
    subject = f" Order Confirmation #{order_id}"
    receipent_data = ShippingAdress.objects.get(user=order.user)
    receipent_email = receipent_data.email
    print("TASK WORKING")
    message=f"Hello your order and payment has been completed successfully. Order ID: {order_id}."

    mail_to_sender = send_mail(subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[receipent_email])

    return mail_to_sender

@shared_task
def send_note(user_id):
    user = User.objects.get(id=user_id)
    
    subject = f" Notification to user: {user.first_name} {user.last_name}"
    receipent_email = user.email
    print("TASK WORKING")
    message=f"Hello, {user.username}. This is a Notification for you, we are worried about yours."

    mail_to_sender = send_mail(subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[receipent_email])

    return mail_to_sender