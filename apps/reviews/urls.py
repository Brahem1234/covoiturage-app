from django.urls import path
from . import views

urlpatterns = [
    path('leave/<int:trip_id>/', views.leave_review, name='leave_review'),
]
