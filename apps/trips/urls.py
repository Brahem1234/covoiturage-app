from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_trips, name='search_trips'),
    path('create/', views.create_trip, name='create_trip'),
    path('my-trips/', views.my_trips, name='my_trips'),
    path('<int:pk>/', views.trip_detail, name='trip_detail'),
    path('<int:pk>/edit/', views.edit_trip, name='edit_trip'),
    path('<int:pk>/delete/', views.delete_trip, name='delete_trip'),
    path('<int:pk>/cancel/', views.cancel_trip, name='cancel_trip'),
]
