from blog.views import PostsListView, PostUniqueView, page, search
from django.urls import path


app_name = 'blog'

urlpatterns = [
    path('', PostsListView.as_view(), name='index'),
    path('page/', page, name='page'),
    path('post/<int:id>/', PostUniqueView.as_view(), name='post'),
    path('search', search, name='search')
]
