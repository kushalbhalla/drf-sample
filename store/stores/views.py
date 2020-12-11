from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Stores

from stores import serializers


class StoresViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage stores in database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Stores.objects.all()
    serializer_class = serializers.StoresSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(store_owner=self.request.user).order_by('-store_name')
