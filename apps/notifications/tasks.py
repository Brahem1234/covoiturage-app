from celery import shared_task
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def send_realtime_notification(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        channel_layer = get_channel_layer()
        group_name = f"user_notifications_{notification.recipient.id}"
        
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "notification": {
                    "id": notification.id,
                    "title": notification.title,
                    "message": notification.message,
                    "link": notification.link,
                    "type": notification.notification_type,
                    "created_at": notification.created_at.isoformat()
                }
            }
        )
    except Notification.DoesNotExist:
        pass
