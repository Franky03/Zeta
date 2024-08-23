from typing import Any
from blog.models import Post
from django.db.models import Q

from django.views.generic import ListView,DetailView

from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render

def handler404(request, template_name="blog/pages/404.html"):
    response = render(template_name)
    response.status_code = 404
    return response

# Create your views here.
def index(request):
    posts = Post.objects.get_posts()
    # SELECT * FROM posts ORDER BY created_at DESC 

    return render(request, 'blog/pages/index.html', {'posts': posts, 'page_title': "Home / "})

class PostsListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = "-created_at"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': "Home / ",
        })
        return context


class PostUniqueView(DetailView):

    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post = self.object  # post object is already available in DetailView as self.object
        post_author = post.author.first_name

        context.update({
            'page_title': f"{post_author} at ",
        })

        return context

    def get_object(self, queryset=None):
        post_id = self.kwargs.get('id')
        post = Post.objects.filter(id=post_id).first()

        if not post:
            raise Http404()

        return post


def page(request):
    return render(request, 'blog/pages/page.html')  

def post(request, id):
    post = Post.objects.get_posts().filter(id=id).first()

    if not post:
        raise Http404()

    return render(request, 'blog/pages/post.html', {'post': post, 'page_title': f"{post.author.first_name} at "})

def search(request):
    search_value = request.GET.get('search', '').strip()

    posts = (
        Post.objects.get_posts().filter(
            Q(content__icontains=search_value)
        )
    )

    return render(request, 'blog/pages/index.html', {'posts': posts, 'search_value': search_value, 'page_title': f"{search_value} — Search / "} )

