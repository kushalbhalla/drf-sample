from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Products, ProductContainer

from stores.serializers import ProductsSerializer

PRODUCTS_URL = reverse('stores:products-list')

def sample_store(user, **params):
    """Create and return sample products"""
    default = {
        'store_name':'Toy Shop',
        'store_type':'playing area',
    }
    default.update(params)

    return Stores.objects.create(store_owner=user,**default)

def sample_products(container_id, **params):
    """Create and return sample products"""
    default = {
        'product_name':"Cricket Bat",
        'product_price':45.90,
        'product_type':"cricket accessories"
    }
    default.update(params)

    return Products.objects.create(connected_container_id=container_id, **default)


class PublicProductsApiTests(TestCase):
    """Test unauthenticated products API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(PRODUCTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductsApiTests(TestCase):
    """Test unauthenticated products API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_products(self):
        """Test retrieving a list of products"""
        self.user2 = get_user_model().objects.create_user(
            'test1@gmail.com',
            'test1pass'
        )

        s1 = sample_store(self.user)
        s2 = sample_store(self.user2)

        p1 = ProductContainer.objects.create(
            store_id=s1,
            container_owner=self.user
        )
        p2 = ProductContainer.objects.create(
            store_id=s2,
            container_owner=self.user2
        )

        sample_products(p1)
        sample_products(p2)

        products = Products.objects.all().order_by('product_id')
        serializer = ProductSerializer(Products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_products_listed_to_user(self):
        """Test retrieving products for user"""
        user2 = get_user_model().objects.create_user(
            'another@gmail.com',
            'pass123'
        )

        s1 = sample_store(self.user)
        s2 = sample_store(self.user2)
        p1 = ProductContainer.objects.create(
            store_id=s1,
            container_owner=self.user
        )
        p2 = ProductContainer.objects.create(
            store_id=s2,
            container_owner=self.user2
        )

        sample_products(p1)
        sample_products(p2)

        res = self.client.get(PRODUCTS_URL)

        products = Products.objects.filter(user=self.user)
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializers.data)
