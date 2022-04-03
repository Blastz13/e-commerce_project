from django.test import TestCase, Client
from django.urls import reverse
from .models import CategoryFeed, Feed, Tag, ContactAddress


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_page_url = reverse('HomePage')

    def test_HomePage_get(self):
        response = self.client.get(self.home_page_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_FeedDetail_get(self):
        response = self.client.get(reverse('FeedDetail', kwargs=[]))
        core1 = Feed.objects.create(
        )


        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'core/blog-post-img.html')
