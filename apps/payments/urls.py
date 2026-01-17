from django.urls import path
from . import views

urlpatterns = [
    path('initiate/<int:booking_id>/', views.initiate_payment, name='initiate_payment'),
    path('create-checkout-session/<int:booking_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('detail/<int:payment_id>/', views.payment_detail, name='payment_detail'),
    path('my-payments/', views.my_payments, name='my_payments'),
]
