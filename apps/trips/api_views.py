from rest_framework import viewsets, permissions
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Trip
from .serializers import TripSerializer
from .choices import get_addresses_for_governorate

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)

@require_GET
def get_governorate_addresses(request, governorate_code):
    """
    Retourne les adresses d'un gouvernorat sous forme JSON.
    """
    addresses = get_addresses_for_governorate(governorate_code)
    return JsonResponse({'addresses': addresses})
