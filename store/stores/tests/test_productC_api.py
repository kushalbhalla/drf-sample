from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import ProductContainer, Products, Stores
from stores.serializers import ProductContainerSerializer

PRODUCTS_CON_URL = reverse('stores:productContainer-list')

def sample_store(user, **params):
    """Create and return sample products"""
    default = {
        'store_name':'Toy Shop',
        'store_type':'playing area',
    }
    default.update(params)

    return Stores.objects.create(store_owner=user,**default)


class PublicProductsApiTests(TestCase):
    """Test unauthenticated products API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(PRODUCTS_CON_URL)

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

    def test_retrieve_products_container(self):
        """Test retrieving a list of products"""
        self.user2 = get_user_model().objects.create_user(
            'test1@gmail.com',
            'test1pass'
        )

        s1 = sample_store(self.user)
        s2 = sample_store(self.user2)
        ProductContainer.objects.create(
            store_id=s1,
            container_owner=self.user
        )
        ProductContainer.objects.create(
            store_id=s2,
            container_owner=self.user2
        )

        products = ProductContainer.objects.all().order_by('container_id')
        serializer = ProductSerializer(Products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_product_container_limited_to_user(self):
        """Test retrieving product container for user"""
        user2 = get_user_model().objects.create_user(
            'test2@gmail.com',
            'test2pass'
        )

        s1 = sample_store(self.user)
        s2 = sample_store(self.user2)
        ProductContainer.objects.create(
            store_id=s1,
            container_owner=self.user
        )
        ProductContainer.objects.create(
            store_id=s2,
            container_owner=self.user2
        )

        res = self.client.get(PRODUCTS_CON_URL)

        products_con = ProductContainer.objetcs.filter(user=self.user)
        serialier = ProductContainerSerializer(products_con, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serialier.data)
