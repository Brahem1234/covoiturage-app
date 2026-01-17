from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.RateLimitedLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/@<str:username>/', views.public_profile, name='public_profile'),
    path('verify-identity/', views.verify_identity, name='verify_identity'),
]
