from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_moderation_email(post, status, moderator_note=None):
    """Send email notification about post moderation status"""
    subject = f'Your post "{post.title}" has been {status}'
    
    context = {
        'post': post,
        'status': status,
        'moderator_note': moderator_note,
        'site_name': 'DJ Blog'
    }
    
    # Render email templates
    html_message = render_to_string('blog/emails/moderation_notification.html', context)
    plain_message = render_to_string('blog/emails/moderation_notification.txt', context)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[post.author.email],
        html_message=html_message,
        fail_silently=False
    )