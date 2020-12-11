from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stores import views

router = DefaultRouter()
router.register('store_list', views.StoresViewSet)

app = 'stores'

urlpatterns = [
    path('', include(router.urls))
]
