from .models import Notification
from .tasks import send_realtime_notification

def create_notification(recipient, notification_type, title, message, link=None):
    """
    Crée une notification pour un utilisateur et l'envoie en temps réel via Celery/Channels.
    """
    notification = Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        link=link
    )
    
    # Envoyer la notification en temps réel via Celery
    send_realtime_notification.delay(notification.id)
    return notification
