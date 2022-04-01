from django.conf.urls.static import static
from django.urls import path

from core.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='HomePage'),
    path('contact/', LeaveMessage.as_view(), name='LeaveMessage'),
    path('blog/', FeedList.as_view(), name='FeedList'),
    path('blog/tag/<str:slug>/', FeedListTag.as_view(), name='FeedListTag'),
    path('blog/<str:category>/', FeedListCategory.as_view(), name='FeedListCategory'),
    path('blog/<str:category>/<str:slug>/', FeedDetail.as_view(), name='FeedDetail'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
