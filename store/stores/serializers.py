from rest_framework import serializers
from core.models import Stores, ProductContainer, Products


class StoresSerializer(serializers.ModelSerializer):
    """Serializer for stores objects"""

    class Meta:
        model = Stores
        fields = '__all__'
        read_only_fields = ('store_id',)


class ProductContainerSerializer(serializers.ModelSerializer):
    """serializer for products container objects"""

    store_id = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Stores.objects.all()
    )

    class Meta:
        model = ProductContainer
        fields = ('container_id', 'store_id', 'container_owner')
        read_only_fields = ('container_id',)

class ProductsSerializer(serializers.ModelSerializer):
    """Serializer for products objects"""

    connected_container_id = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = ProductContainer.objects.all()
    )

    class Meta:
        model = Products
        fields = ('product_id', 'product_name', 'product_price', 'product_type', 'connected_container_id')
        read_only_fields = ('product_id',)
