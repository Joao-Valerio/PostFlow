from django.core.mail import send_mail
from django.conf import settings

from .models import Notification


def create_notification(user, title, message, notification_type=Notification.Type.INFO, organization=None, metadata=None):
    return Notification.objects.create(
        user=user,
        organization=organization or getattr(user, "organization", None),
        type=notification_type,
        title=title,
        message=message,
        metadata=metadata or {},
    )


def notify_publish_failure(user, post_title, error_message):
    notification = create_notification(
        user=user,
        title="Falha na publicação",
        message=f'O post "{post_title}" falhou: {error_message}',
        notification_type=Notification.Type.FAILURE,
    )
    if user.email:
        send_mail(
            subject="PostFlow — Falha na publicação",
            message=notification.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
    return notification


def notify_publish_success(user, post_title, platform):
    return create_notification(
        user=user,
        title="Publicação realizada",
        message=f'O post "{post_title}" foi publicado em {platform}.',
        notification_type=Notification.Type.SUCCESS,
    )


def get_unread_notifications(user, limit=10):
    return Notification.objects.filter(user=user, is_read=False)[:limit]
