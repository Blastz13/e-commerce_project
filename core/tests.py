from django.test import TestCase, Client
from django.urls import reverse
from .models import Feed, CategoryFeed, Comment, Tag


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

    def test_create_comment_FeedDetail(self):
        """Checking the creation of a news comment"""
        response = self.client.post(self.feed.get_absolute_url(), data={"email": "test@mail.ru",
                                                                        "name": "Test_User", "text": "Good Luck!"})
        comment = Comment.objects.get(email="test@mail.ru", name="Test_User")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(comment), "Test_User - Hot news")

    def tearDown(self):
        self.feed.delete()
        self.category.delete()


class TestFeedList(TestCase):
    def setUp(self):
        self.client = Client()

    def test_FeedList_get(self):
        """Page retrieval check FeedList"""
        response = self.client.get(reverse('FeedList'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/blog.html')


class TestFeedListCategory(TestCase):
    def setUp(self):
        self.cateforyfeed = CategoryFeed.objects.create(title="Test_Category", slug="test_category")

    def test_FeedListCategory_get(self):
        """Page retrieval check FeedListCategory"""
        response = self.client.get(self.cateforyfeed.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/blog.html')

    def tearDown(self):
        self.cateforyfeed.delete()


class TestFeedListTag(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(title="Test_Tag", slug="test_tag")

    def test_FeedListTag_get(self):
        """Page retrieval check FeedListTag"""
        response = self.client.get(self.tag.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/blog-filter-by-tags.html')

    def tearDown(self):
        self.tag.delete()