from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import CustomUser

def send_email_confirmation(user: CustomUser):
    confirmation_code = get_random_string(32)
    user.confirmation_code = confirmation_code
    user.save()

    send_mail(
        "Confirm your email",
        f"Your confirmation code: {confirmation_code}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
