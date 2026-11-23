from rest_framework import viewsets

from .models import Property
from .permissions import IsHostOrReadOnly
from .serializers import PropertySerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.select_related("host").all()
    serializer_class = PropertySerializer
    permission_classes = [IsHostOrReadOnly]
    filterset_fields = ("location", "is_active", "host")
    search_fields = ("title", "description", "location")
    ordering_fields = ("price_per_night", "created_at")
