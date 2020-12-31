from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stores import views

router = DefaultRouter()
router.register('stores', views.StoresViewSet)

app_name = 'stores'

urlpatterns = [
    path('', include(router.urls)),
]
