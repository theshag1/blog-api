from users.models import User
from django.test import TestCase
from .models import Blog, Category


# Create your tests here.

class BlogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='sdgfj@email.com', password='shgjkdagi')
        self.category = Category.objects.create(name='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog',
            slug='test-blog',
            author=self.user,
            blog_body='Test blog body',
            category=self.category,
            blog_interesting='Interesting'
        )

    def test_blog_model(self):
        self.assertEqual(self.blog.title, 'Test Blog')
        self.assertEqual(self.blog.slug, 'test-blog')
        self.assertEqual(self.blog.author, self.user)
        self.assertEqual(self.blog.blog_body, 'Test blog body')
        self.assertEqual(self.blog.category, self.category)
        self.assertEqual(self.blog.blog_interesting, 'Interesting')

    def test_blog_str_method(self):
        self.assertEqual(str(self.blog), 'Test Blog')

    def tearDown(self):
        self.blog.delete()
        self.category.delete()
        self.user.delete()
