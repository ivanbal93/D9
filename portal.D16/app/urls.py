from django.urls import path
from .views import PostList, PostDetail, Search, NewPost, PostUpdate, PostDelete, SubscribeView
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60*1) (PostList.as_view()), name='post_list'),
    path('<int:pk>', cache_page(60*5) (PostDetail.as_view()), name='post_detail'),
    path('search', Search.as_view(), name='search'),
    path('create', NewPost.as_view(), name='create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('subscribe/<int:category_id>', SubscribeView.as_view(), name='add_subscriber'),
    # path('celery_test', IndexView.as_view())
]