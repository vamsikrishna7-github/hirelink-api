from django.core.mail import send_mail
from django.conf import settings

def send_password_reset_email(user, uid, token):
    reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"  # Replace with your frontend reset URL
    subject = "Reset Your Password"
    message = f"""
    Hi {user.name or user.email},

    Please click the link below to reset your password:
    {reset_link}

    If you didn't request this, you can ignore this email.
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
