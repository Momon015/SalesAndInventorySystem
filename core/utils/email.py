from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings


def send_email(email, otp):
    subject = 'Verify your OTP Code'
    text_context = f"Your OTP is {otp}. It expires in 5 minutes."
    html_context = f"""
    <p> Your OTP code is:</p>
    <h2>{otp}</h2>
    <p>This code expires in 5 minutes.</p>  
    """
    message = EmailMultiAlternatives(
        subject=subject,
        body=text_context,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )
    
    message.attach_alternative(html_context, 'text/html')
    message.send()
    