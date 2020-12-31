from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Stores

from stores import serializers


class StoresViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage stores in database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Stores.objects.all()
    serializer_class = serializers.StoresSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter().order_by('-store_name')

    def perform_create(self, serializer):
        """Create a new store"""
        serializer.save(store_owner= self.request.user)
