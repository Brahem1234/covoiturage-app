from .models import Notification

def create_notification(recipient, notification_type, title, message, link=None):
    """
    Crée une notification pour un utilisateur.
    """
    Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        link=link
    )
