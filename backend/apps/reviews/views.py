from rest_framework import viewsets

from .models import Review
from .permissions import IsReviewAuthorOrAdminOrReadOnly
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("author", "property").all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrAdminOrReadOnly]
    filterset_fields = ("property", "rating")
    ordering_fields = ("rating", "created_at")
