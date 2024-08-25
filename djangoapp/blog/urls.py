from blog.views import PostsListView, PostUniqueView, search, repost_page,repost,repost_directly, ToggleLikeView,CreateCommentView, CreatePostView
from django.urls import path


app_name = 'blog'

urlpatterns = [
    path('', PostsListView.as_view(), name='index'),
    path('post/<int:id>/', PostUniqueView.as_view(), name='post'),
    path('search', search, name='search'),
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    path('comment/', CreateCommentView.as_view(), name='comment'),
    path('repost_page/<int:id>', repost_page, name='repost_page'),
    path('repost/', repost, name='repost'),
]

htmx_urlpatterns = [
    path('post/<int:post_id>/like/', ToggleLikeView.as_view(), name='toggle_like'),
    path('repost_directly/<int:pid>', repost_directly, name='repost_directly'),
]

urlpatterns += htmx_urlpatterns