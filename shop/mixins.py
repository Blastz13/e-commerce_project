from django.core.paginator import Paginator
from django.db.models import Q


class ObjectSortPaginate:
    def get_pagination(self, all_products, count=12, obj_selected_category=None):

        paginator = Paginator(all_products, count)
        number_page = self.request.GET.get('page', 1)
        products_page = paginator.get_page(number_page)
        is_has_other_page = products_page.has_other_pages()
        # if query_search_user_feed:
        #     query_search_feed = f"&search-feed={query_search_user_feed}"
        # else:
        #     query_search_feed = ""

        if products_page.has_previous():
            prev_page = f"?page={products_page.previous_page_number()}"
        else:
            prev_page = ""

        if products_page.has_next():
            next_page = f"?page={products_page.next_page_number()}"
        else:
            next_page = ""

        return {'products_all': products_page,
                # 'query_search_feed': query_search_feed,
                # 'query_search_user': query_search_user_feed,
                'is_has_other_page': is_has_other_page,
                'next_page': next_page,
                'prev_page': prev_page}