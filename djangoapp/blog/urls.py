from blog.views import PostsListView, PostUniqueView, page, search,create_post, create_comment, toggle_like
from django.urls import path


app_name = 'blog'

urlpatterns = [
    path('', PostsListView.as_view(), name='index'),
    path('page/', page, name='page'),
    path('post/<int:id>/', PostUniqueView.as_view(), name='post'),
    path('search', search, name='search'),
    path('create-post/', create_post, name='create_post'),
    path('comment/', create_comment, name='comment'),
]

htmx_urlpatterns = [
    path('post/<int:post_id>/like/', toggle_like, name='toggle_like'),
]

urlpatterns += htmx_urlpatterns