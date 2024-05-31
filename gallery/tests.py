# gallery/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from gallery.models import Category, Image
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
import os

class GalleryViewTests(TestCase):
    def setUp(self):
        # Створення тестового користувача
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Створення тестових даних
        self.category = Category.objects.create(name='TestCategory')
        
        # Створення тимчасового зображення
        temp_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        with open(temp_image, 'wb') as f:
            f.write(os.urandom(1024))  # заповнення файлу випадковими даними
        
        self.image = Image.objects.create(
            title='TestImage',
            image=SimpleUploadedFile(name='test_image.jpg', content=open(temp_image, 'rb').read(), content_type='image/jpeg'),
            created_date='2023-01-01',
            age_limit=0
        )
        self.image.categories.add(self.category)
        os.remove(temp_image)

    def test_gallery_view(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestCategory')
        self.assertTemplateUsed(response, 'gallery.html')

    def test_image_detail_view(self):
        response = self.client.get(reverse('image_detail', args=[self.image.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestImage')
        self.assertTemplateUsed(response, 'image_detail.html')
