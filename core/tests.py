from django.test import TestCase, Client
from django.urls import reverse
from .models import Feed, CategoryFeed, Comment, Tag, ContactForm


class TestViewHomePage(TestCase):
    def setUp(self):
        self.client = Client()

    def test_request_get(self):
        """Page retrieval check HomePage"""
        response = self.client.get(reverse('HomePage'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')


class TestViewFeedDetail(TestCase):
    def setUp(self):
        self.category = CategoryFeed.objects.create(title="HOT_NEWS", slug="hot_news")
        self.feed = Feed.objects.create(title="Hot news", body="Lorem Ipsum", slug="hot_news",
                                        category=self.category, is_slider=True, is_publish=True, is_blog=True)

    def test_request_get(self):
        """Page retrieval check FeedDetail"""
        response = self.client.get(self.feed.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/blog-post-img.html')

    def test_create_comment_post(self):
        """Checking the creation of a news comment"""
        response = self.client.post(self.feed.get_absolute_url(), data={
            "email": "test@mail.ru",
            "name": "Test_User",
            "text": "Good Luck!"
        })
        comment = Comment.objects.get(email="test@mail.ru", name="Test_User")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(comment), "Test_User - Hot news")

    def test_create_comment_with_parent_post(self):
        """Checking the creation of news comment with parent"""
        comment_parent = Comment.objects.create(email="test1@mail.ru", name="Test_User1", feed=self.feed)
        response = self.client.post(self.feed.get_absolute_url(), data={
            "email": "test2@mail.ru",
            "name": "Test_User2",
            "text": "Good Luck2!",
            "parent": comment_parent.id
        })

        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(Comment.objects.get(email="test2@mail.ru", name="Test_User2", text="Good Luck2!",
                                                 parent=comment_parent.id))

    def tearDown(self):
        self.feed.delete()
        self.category.delete()


class TestViewFeedList(TestCase):
    def setUp(self):
        self.client = Client()

    def test_request_get(self):
        """Page retrieval check FeedList"""
        response = self.client.get(reverse('FeedList'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/blog.html')


class TestViewFeedListCategory(TestCase):
    def setUp(self):
        self.category_feed = CategoryFeed.objects.create(title="Test_Category", slug="test_category")

    def test_request_get(self):
        """Page retrieval check FeedListCategory"""
        response = self.client.get(self.category_feed.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/blog.html')

    def tearDown(self):
        self.category_feed.delete()


class TestViewFeedListTag(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(title="Test_Tag", slug="test_tag")

    def test_request_get(self):
        """Page retrieval check FeedListTag"""
        response = self.client.get(self.tag.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/blog-filter-by-tags.html')

    def tearDown(self):
        self.tag.delete()


class TestViewLeaveMessage(TestCase):
    def test_request_get(self):
        """Page retrieval check LeaveMessage"""
        response = self.client.get(reverse('LeaveMessage'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')

    def test_send_contact_message_post(self):
        """"Checking contact message creation"""
        response = self.client.post(reverse('LeaveMessage'), data={
            "email": "test@mail.ru",
            "name": "Test_User",
            "subject": "Test_Subject",
            "message": "Good Luck!"
        })
        contact = ContactForm.objects.get(email="test@mail.ru", name="Test_User")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(contact), "test@mail.ru - Test_Subject")


class TestModelFeed(TestCase):
    def setUp(self):
        self.category = CategoryFeed.objects.create(title="HOT_NEWS", slug="hot_news")
        self.feed = Feed.objects.create(title="Hot news", body="Lorem Ipsum", slug="hot_news",
                                        category=self.category, is_slider=True, is_publish=True, is_blog=True)
        self.comment1 = Comment.objects.create(email="test1@mail.ru", name="Test_User1", feed=self.feed)
        self.comment2 = Comment.objects.create(email="test2@mail.ru", name="Test_User2", feed=self.feed)

    def test_get_abolute_url(self):
        """Test geting url of Feed"""
        self.assertEqual(self.feed.get_absolute_url(), '/blog/hot_news/hot_news/')

    def test_get_comment(self):
        """Test getting comments in Feed"""
        self.assertCountEqual({self.comment1, self.comment2}, self.feed.get_comments())

    def test_str(self):
        """Test cast Feed to string"""
        self.assertEqual(str(self.feed), "Hot news")

    def tearDown(self):
        self.category.delete()
        self.feed.delete()
        self.comment2.delete()
        self.comment1.delete()
