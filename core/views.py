from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.utils import timezone
from django.views.generic import View
from django.conf import settings

from .forms import CommentForm, MessageContactForm

from .models import CategoryFeed, Feed, Tag, ContactAddress
from shop.models import SpecialCategoryProduct

from .mixins import ObjectSortPaginate


class HomePage(View):
    def get(self, request):
        slider_feeds = Feed.objects.filter(is_publish=True,
                                           is_slider=True,
                                           date_published_from__lte=datetime.now(tz=timezone.utc),
                                           date_published_to__gte=datetime.now(tz=timezone.utc))

        small_feeds = Feed.objects.filter(is_publish=True,
                                          is_blog=True,
                                          date_published_from__lte=datetime.now(tz=timezone.utc),
                                          date_published_to__gte=datetime.now(tz=timezone.utc))

        return render(request, 'core/index.html', context={"feeds": slider_feeds,
                                                           "small_feeds": small_feeds,
                                                           'special_categories_products': SpecialCategoryProduct
                                                                                          .objects.all()})


class FeedDetail(View):
    def get(self, request, category, slug):
        comment_form = CommentForm()
        feed = get_object_or_404(Feed,
                                 category__slug__iexact=category,
                                 slug__iexact=slug,
                                 is_publish=True,
                                 is_blog=True,
                                 date_published_from__lte=datetime.now(tz=timezone.utc))

        try:
            next_obj_feed = feed.get_next_by_date_publicate(is_publish=True,
                                                            is_blog=True,
                                                            date_published_from__lte=datetime.now(tz=timezone.utc))
        except Feed.DoesNotExist:
            next_obj_feed = None

        try:
            previuos_obj_feed = feed.get_previous_by_date_publicate(is_publish=True,
                                                                    is_blog=True,
                                                                    date_published_from__lte=datetime.now(
                                                                        tz=timezone.utc))
        except Feed.DoesNotExist:
            previuos_obj_feed = None

        return render(request, 'core/blog-post-img.html', context={'feed': feed,
                                                                   'comment_form': comment_form,
                                                                   'next_feed': next_obj_feed,
                                                                   'previous_feed': previuos_obj_feed,
                                                                   })

    def post(self, request, category, slug):
        feed = get_object_or_404(Feed,
                                 category__slug__iexact=category,
                                 slug=slug)

        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.feed = feed
            form.save()
        return redirect(feed.get_absolute_url())


class FeedList(ObjectSortPaginate, View):
    def get(self, request):
        all_feeds = Feed.objects.filter(is_publish=True,
                                        is_blog=True,
                                        date_published_from__lte=datetime.now(tz=timezone.utc))

        return render(request, 'core/blog.html', context=self.get_pagination(all_feeds))


class FeedListCategory(ObjectSortPaginate, View):
    def get(self, request, category):
        obj_selected_category = get_object_or_404(CategoryFeed, slug__iexact=category)

        all_feeds = Feed.objects.filter(category__slug__iexact=category,
                                        is_publish=True,
                                        is_blog=True,
                                        date_published_from__lte=datetime.now(tz=timezone.utc))

        return render(request, 'core/blog.html', context=self.get_pagination(all_feeds, obj_selected_category))


class FeedListTag(ObjectSortPaginate, View):
    def get(self, request, slug):
        obj_selected_category = get_object_or_404(Tag, slug__iexact=slug)

        feeds_all = Feed.objects.filter(tag__slug__iexact=slug,
                                        is_publish=True,
                                        is_blog=True,
                                        date_published_from__lte=datetime.now(tz=timezone.utc))

        return render(request, 'core/blog-filter-by-tags.html',
                      context=self.get_pagination(feeds_all, obj_selected_category))


class LeaveMessage(View):
    def get(self, request):
        form = MessageContactForm()
        contact_address = ContactAddress.objects.all()

        return render(request, 'core/contact.html', context={'form': form,
                                                             'contact_address': contact_address})

    def post(self, request):
        form = MessageContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject'] + ' от ' + form.cleaned_data['email']
            send_mail(subject=subject, message=form.cleaned_data['message'],
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=['sinicinr2003@mail.ru'])

            form.save()
        return redirect('HomePage')
