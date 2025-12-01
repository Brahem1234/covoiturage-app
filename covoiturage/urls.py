from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.trips.urls')),  # La page d'accueil sera gérée par trips
    path('users/', include('apps.users.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('messaging/', include('apps.messaging.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('payments/', include('apps.payments.urls')),
    path('notifications/', include('apps.notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
