from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('send/<int:recipient_id>/', views.send_message, name='send_message'),
    path('<int:pk>/', views.message_detail, name='message_detail'),
    path('conversation/<int:user_id>/', views.conversation, name='conversation'),
]
