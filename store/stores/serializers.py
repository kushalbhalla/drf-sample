from rest_framework import serializers
from core.models import Stores


class StoresSerializer(serializers.ModelSerializer):
    """Serializer for stores objects"""

    class Meta:
        models = Stores
        fields = '__all__'
        read_only_fields = ('store_id',)
