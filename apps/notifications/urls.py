from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notifications'),
    path('<int:notification_id>/read/', views.mark_as_read, name='mark_notification_read'),
    path('read-all/', views.mark_all_as_read, name='mark_all_notifications_read'),
]
