from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Stores

STORES_URL = reverse('stores:stores-list')

class PublicStoresApiTests(TestCase):
    """Test the publicly available stores API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving stores"""
        res = self.client.get(STORES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStoresApiTests(TestCase):
    """Test the authorized user stores API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@london.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        def test_retrieve_stores(self):
            """Test retrieving stores"""
            Stores.objects.create(
                store_owner=self.user,
                store_name='Toy Shop',
                store_type='playing area',
            )
            Stores.objects.create(
                store_owner=self.user,
                store_name='Kite shop',
                store_type='Design stuff',
            )
            res = self.client.get(STORES_URL)

            stores = Stores.objects.all().order_by('-name')
            serializer = StoresSerializer(stores, many=True)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, serializer.data)

        def test_stores_limited_to_user(self):
            """Test that tags returned are for the authentication user"""
            user = get_user_model().objects.create_user(
                'other@london.com',
                'testpass'
            )
            Stores.objects.create(store_owner=user, store_name='Toy Shop', store_type='playing area')
            store = Stores.objects.create(store_owner=self.user, store_name='Tweet', store_type='cafe')

            res = self.client.get(STORES_URL)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(lem(res.data), 1)
            self.assertEqual(res.data[0]['store_name'], store.store_name)

        def test_create_stores_successful(self):
            """Test creating a new store"""
            payload = {'store_name':'Tweet', 'store_type':'cafe'}
            self.client.post(STORES_URL, payload)

            exists = Stores.objects.filter(
                store_owner=self.user,
                store_name=payload['store_name']
            ).exists()
            self.assertTrue(exists)

        def test_create_stores_invalid(self):
            """Test creating a new store with invalid payload"""
            payload = {'store_name':'Tweet','store_type':''}
            res = self.client.post(STORES_URL, payload)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
