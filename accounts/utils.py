from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse


def send_password_reset_email(user, uid, token):
    reset_link = f"https://zyukthi.vercel.app/reset-password/{uid}/{token}/"  
    subject = "Reset Your Password"
    message = f"""
    Hi {user.name or user.email},

    Please click the link below to reset your password:
    {reset_link}

    If you didn't request this, you can ignore this email.
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

#health check
def health_check(request):
    return JsonResponse({'status': 'ok'}, status=200)

