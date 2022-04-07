from django.test import TestCase, Client
from django.urls import reverse
from .models import Feed, CategoryFeed, Comment, Tag, ContactForm, OurBrand, ContactAddress


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
        self.category = CategoryFeed.objects.create(title="HOT NEWS", slug="hot_news")
        self.feed = Feed.objects.create(title="New book", body="Lorem Ipsum", slug="new_book",
                                        category=self.category, is_slider=True, is_publish=True, is_blog=True)

    def test_request_get(self):
        """Page retrieval check FeedDetail"""
        response = self.client.get(self.feed.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/blog-post-img.html')

    def test_create_comment_post(self):
        """Checking the creation of a new comment"""
        response = self.client.post(self.feed.get_absolute_url(), data={
            "email": "ivan_pupkin@mail.ru",
            "name": "Ivan",
            "text": "Good Luck!"
        })
        comment = Comment.objects.get(email="ivan_pupkin@mail.ru", name="Ivan")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(comment), "Ivan - New book")

    def test_create_comment_with_parent_post(self):
        """Checking the creation of news comment with parent"""
        comment_parent = Comment.objects.create(email="ivan_pupkin@mail.ru", name="Ivan", feed=self.feed)
        response = self.client.post(self.feed.get_absolute_url(), data={
            "email": "lena_golovach@mail.ru",
            "name": "Elena",
            "text": "Very bad shop!",
            "parent": comment_parent.id
        })

        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(Comment.objects.get(email="lena_golovach@mail.ru", name="Elena", text="Very bad shop!",
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
        self.category = CategoryFeed.objects.create(title="HOT NEWS", slug="hot_news")

    def test_request_get(self):
        """Page retrieval check FeedListCategory"""
        response = self.client.get(self.category.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/blog.html')

    def tearDown(self):
        self.category.delete()


class TestViewFeedListTag(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(title="Science Fiction", slug="science_fiction")

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
            "email": "ivan_pupkin@mail.ru",
            "name": "Ivan",
            "subject": "THANKS",
            "message": "Good Luck!"
        })
        contact = ContactForm.objects.get(email="ivan_pupkin@mail.ru", name="Ivan")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(contact), "ivan_pupkin@mail.ru - THANKS")


class TestModelFeed(TestCase):
    def setUp(self):
        self.category = CategoryFeed.objects.create(title="HOT NEWS", slug="hot_news")
        self.feed = Feed.objects.create(title="New book", body="Lorem Ipsum", slug="new_book",
                                        category=self.category, is_slider=True, is_publish=True, is_blog=True)
        self.comment1 = Comment.objects.create(email="ivan_pupkin@mail.ru", name="Ivan", feed=self.feed)
        self.comment2 = Comment.objects.create(email="lena_golovach@mail.ru", name="Elena", feed=self.feed)

    def test_get_abolute_url(self):
        """Test geting url of Feed"""
        self.assertEqual(self.feed.get_absolute_url(), '/blog/hot_news/new_book/')

    def test_get_comment(self):
        """Test getting comments in Feed"""
        self.assertCountEqual({self.comment1, self.comment2}, self.feed.get_comments())

    def test_str(self):
        """Test cast Feed to string"""
        self.assertEqual(str(self.feed), "New book")

    def tearDown(self):
        self.category.delete()
        self.feed.delete()
        self.comment2.delete()
        self.comment1.delete()


class TestModelCategoryFeed(TestCase):
    def setUp(self):
        self.category = CategoryFeed.objects.create(title="HOT NEWS", slug="hot_news")

    def test_get_absolute_url(self):
        """Test geting url of CategoryFeed"""
        self.assertEqual(self.category.get_absolute_url(), '/blog/hot_news/')

    def test_str(self):
        """Test cast CategoryFeed to string"""
        self.assertEqual(str(self.category), "HOT NEWS")

    def tearDown(self):
        self.category.delete()


class TestModelTag(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(title="Science Fiction", slug="science_fiction")

    def test_get_absolute_url(self):
        """Test geting url of Tag"""
        self.assertEqual(self.tag.get_absolute_url(), '/blog/tag/science_fiction/')

    def test_str(self):
        """Test cast Tag to string"""
        self.assertEqual(str(self.tag), "Science Fiction")

    def tearDown(self):
        self.tag.delete()


class TestModelComment(TestCase):
    def test_str(self):
        """Test cast Comment to string"""
        self.category = CategoryFeed.objects.create(title="HOT NEWS", slug="hot_news")
        self.feed = Feed.objects.create(title="New book", body="Lorem Ipsum", slug="new_book",
                                        category=self.category, is_slider=True, is_publish=True, is_blog=True)
        self.comment = Comment.objects.create(email="ivan_pupkin@mail.ru", name="Ivan", feed=self.feed)
        self.assertEqual(str(self.comment), "Ivan - New book")


class TestOurBrand(TestCase):
    def test_str(self):
        """Test cast Brand to string"""
        self.brand = OurBrand.objects.create(title="Abibas")
        self.assertEqual(str(self.brand), "Abibas")


class TestContactForm(TestCase):
    def test_str(self):
        """Test cast ContactForm to string"""
        self.email_message = ContactForm.objects.create(name="Ivan", email="ivan_pupkin@mail.ru", subject="THANKS!",
                                                        message="Good luck!")
        self.assertEqual(str(self.email_message), "ivan_pupkin@mail.ru - THANKS!")


class TestContactAddress(TestCase):
    def test_str(self):
        """Test cast ContactAddress to string"""
        self.contact_adress = ContactAddress.objects.create(title="Our contacts in Moscow",
                                                            address="Prospect Vernadskogo,78", phone="+7-909-09-09",
                                                            email="best_book_shop@mail.ru")
        self.assertEqual(str(self.contact_adress), "Prospect Vernadskogo,78 - +7-909-09-09, best_book_shop@mail.ru")
