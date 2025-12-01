from django.urls import path
from . import views

urlpatterns = [
    path('initiate/<int:booking_id>/', views.initiate_payment, name='initiate_payment'),
    path('process/<int:payment_id>/', views.process_payment, name='process_payment'),
    path('card/<int:payment_id>/', views.process_card_payment, name='process_card_payment'),
    path('success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('detail/<int:payment_id>/', views.payment_detail, name='payment_detail'),
    path('my-payments/', views.my_payments, name='my_payments'),
]
