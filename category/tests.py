from django.test import TestCase
from django.test import TestCase
from .models import Category


# Create your tests here.


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', position=1)

    def test_category_model(self):
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.position, 1)

    def test_category_str_method(self):
        self.assertEqual(str(self.category), 'Test Category')

    def tearDown(self):
        self.category.delete()
