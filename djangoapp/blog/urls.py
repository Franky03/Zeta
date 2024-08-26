from blog.views import repost_page,repost,repost_directly,update_post_pre,update_post_pos, delete_post,update_comment_pos,update_comment_pre,delete_comment, register,custom_login, logout_view
from blog.views import ToggleLikeView,CreateCommentView, CreatePostView,profile
from blog.views import SearchListView,PostsListView,  PostUniqueView
from django.urls import path
from django.contrib.auth.decorators import login_required


app_name = 'blog'

urlpatterns = [
    path('', login_required(PostsListView.as_view(), login_url="blog:login"), name='index'),
    path('login/', custom_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', login_required(logout_view, login_url="blog:login"), name='logout'),
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
    path('update_post_pos/', update_post_pos, name='update_post_pos'),
    path('delete_post/<int:pid>', delete_post, name='delete_post'),
    path('update_comment_pos/', update_comment_pos, name='update_comment_pos'),
    path('update_comment_pre/<int:cpk>', update_comment_pre, name='update_comment_pre'),
    path('delete_comment/', delete_comment, name='delete_comment'),
    path('profile/', profile, name='profile'),
]

urlpatterns += htmx_urlpatterns