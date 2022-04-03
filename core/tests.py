from django.test import TestCase, Client
from django.urls import reverse
from .models import Feed, CategoryFeed


class TestHomePage(TestCase):
    def setUp(self):
        self.client = Client()

    def test_HomePage_get(self):
        """Page retrieval check HomePage"""
        response = self.client.get(reverse('HomePage'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')


class TestFeedDetail(TestCase):
    def setUp(self):
        self.category = CategoryFeed.objects.create(title="HOT_NEWS", slug="hot_news")
        self.feed = Feed.objects.create(title="Hot news", body="Lorem Ipsum", slug="hot_news",
                                        category=self.category, is_slider=True, is_publish=True, is_blog=True)

    def test_FeedDetail_get(self):
        """Page retrieval check FeedDetail"""
        response = self.client.get(self.feed.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/blog-post-img.html')

    def tearDown(self):
        self.feed.delete()
        self.category.delete()
