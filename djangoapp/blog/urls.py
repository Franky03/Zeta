from blog.views import PostsListView, PostUniqueView, page, search,create_post, create_comment, toggle_like, repost_page,repost,repost_directly
from django.urls import path


app_name = 'blog'

urlpatterns = [
    path('', PostsListView.as_view(), name='index'),
    path('page/', page, name='page'),
    path('post/<int:id>/', PostUniqueView.as_view(), name='post'),
    path('search', search, name='search'),
    path('create-post/', create_post, name='create_post'),
    path('comment/', create_comment, name='comment'),
    path('repost_page/<int:id>', repost_page, name='repost_page'),
    path('repost/', repost, name='repost'),
]

htmx_urlpatterns = [
    path('post/<int:post_id>/like/', toggle_like, name='toggle_like'),
    path('repost_directly/<int:pid>', repost_directly, name='repost_directly'),
]

urlpatterns += htmx_urlpatterns