from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email='test@london.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successfull"""
        # username = 'kally'
        email = 'test@london.com'
        password = 'test1234'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_noremalized(self):
        """Test the email for a new user is noremalized"""
        email = 'test@LONDON.com'
        user = get_user_model().objects.create_user(email, 'test1234')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@lead.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_store_name_str(self):
        """Test the store must be a string """
        store = models.Stores.objects.create(
            store_owner=sample_user(),
            store_name='Toy Shop',
            store_type='playing area',

        )

        self.assertEqual(str(store), store.store_name)

    def test_product_str(self):
        """Test the recipe string representation"""
        products = models.Products.objects.create(
            product_name="Cricket Bat",
            product_price=45.90,
            product_type="cricket accessories"
        )
    
        self.assertEqual(str(products), products.product_name)
