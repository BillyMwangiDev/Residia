from rest_framework import serializers

from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    host_id = serializers.IntegerField(source="host.id", read_only=True)
    host_name = serializers.CharField(source="host.full_name", read_only=True)

    class Meta:
        model = Property
        fields = (
            "id",
            "host_id",
            "host_name",
            "title",
            "description",
            "location",
            "price_per_night",
            "bedrooms",
            "bathrooms",
            "max_guests",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "host_id", "host_name", "created_at", "updated_at")

    def create(self, validated_data):
        validated_data["host"] = self.context["request"].user
        return super().create(validated_data)
