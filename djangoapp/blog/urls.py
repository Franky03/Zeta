from blog.views import repost_page,repost,repost_directly,update_post_pre,update_post_pos, delete_post
from blog.views import ToggleLikeView,CreateCommentView, CreatePostView
from blog.views import SearchListView,PostsListView,  PostUniqueView
from django.urls import path


app_name = 'blog'

urlpatterns = [
    path('', PostsListView.as_view(), name='index'),
    path('post/<int:id>/', PostUniqueView.as_view(), name='post'),
    path('search', SearchListView.as_view(), name='search'),
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    path('comment/', CreateCommentView.as_view(), name='comment'),
    path('repost_page/<int:id>', repost_page, name='repost_page'),
    path('repost/', repost, name='repost'),
]

htmx_urlpatterns = [
    path('post/<int:post_id>/like/', ToggleLikeView.as_view(), name='toggle_like'),
    path('repost_directly/<int:pid>', repost_directly, name='repost_directly'),
    path('update_post_pre/<int:pid>', update_post_pre, name='update_post_pre'),
    path('update_post_pos/<int:pid>', update_post_pos, name='update_post_pos'),
    path('delete_post/<int:pid>', delete_post, name='delete_post')
]

urlpatterns += htmx_urlpatterns