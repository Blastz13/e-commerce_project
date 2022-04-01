from django.core.paginator import Paginator
from django.db.models import Q


class ObjectSortPaginate:
    def get_pagination(self, feeds_all, obj_selected_category=None, count=4):
        query_search_user_feed = self.request.GET.get('search-feed', '')

        paginator = Paginator(feeds_all.filter(Q(title__icontains=query_search_user_feed) |
                                               Q(body__icontains=query_search_user_feed) |
                                               Q(tag__title__icontains=query_search_user_feed)), count)

        number_page = self.request.GET.get('page', 1)
        feed_page = paginator.get_page(number_page)
        is_has_other_page = feed_page.has_other_pages()

        if query_search_user_feed:
            query_search_feed = f"&search-feed={query_search_user_feed}"
        else:
            query_search_feed = ""

        if feed_page.has_previous():
            prev_page = f"?page={feed_page.previous_page_number()}"
        else:
            prev_page = ""

        if feed_page.has_next():
            next_page = f"?page={feed_page.next_page_number()}"
        else:
            next_page = ""

        return {'feeds_all': feed_page,
                'query_search_feed': query_search_feed,
                'query_search_user': query_search_user_feed,
                'is_has_other_page': is_has_other_page,
                'next_page': next_page,
                'prev_page': prev_page,
                'obj_selected_category': obj_selected_category}
