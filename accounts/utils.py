from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

def send_password_notification(user, notification_type, **kwargs):
    """
    Unified password notification system
    notification_type: 'reset', 'changed', 'created'
    """
    templates = {
        'reset': {
            'subject': 'Password Reset Request',
            'template': 'accounts/emails/password_reset',
        },
        'changed': {
            'subject': 'Password Changed Successfully',
            'template': 'accounts/emails/password_changed',
        },
        'created': {
            'subject': 'Welcome to DJ Blog',
            'template': 'accounts/emails/account_created',
        }
    }
    
    template_config = templates.get(notification_type)
    if not template_config:
        raise ValueError(f"Invalid notification type: {notification_type}")
        
    context = {
        'user': user,
        'timestamp': timezone.now(),
        **kwargs  # Additional context like reset tokens
    }
    
    html_message = render_to_string(f"{template_config['template']}.html", context)
    plain_message = render_to_string(f"{template_config['template']}.txt", context)
    
    return send_mail(
        subject=template_config['subject'],
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False
    )