from typing import Any
from blog.models import Post, Comment, Like
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView

from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def handler404(request, template_name="blog/pages/404.html"):
    response = render(template_name)
    response.status_code = 404
    return response

# Create your views here.
def index(request):
    posts = Post.objects.get_posts()
    # SELECT * FROM posts ORDER BY created_at DESC 

    return render(request, 'blog/pages/index.html', {'posts': posts, 'page_title': "Home / "})

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        if content.strip():
            post = Post.objects.create(author=request.user, content=content)
            
            messages.success(request, 'Post publicado!')
            return redirect('blog:index')
        else:
            messages.error(request, 'O conteúdo do post não pode estar vazio.')
            return redirect('blog:index')

@login_required
def create_comment(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        post_id = request.POST.get('pid', '')
        post_id = int(post_id)
        if content.strip():
            post = Post.objects.filter(id=post_id).first()
            commment = Comment.objects.create(author=request.user, post=post,content=content)
            
            messages.success(request, 'Comentário publicado!')
            return redirect('blog:post', id=post_id)
        else:
            messages.error(request, 'O conteúdo do comentário não pode estar vazio.')
            return redirect('blog:post', id=post_id)
        
@login_required
def toggle_like(request, post_id):
    post = Post.objects.filter(id=post_id).first() # SELECT * FROM post WHERE id = post_id;
    user = request.user

    user = User.objects.filter(username=user).first()
    existing_like = Like.objects.filter(user=user, post=post).first() # SELECT * FROM like WHERE user_id = user_id AND post_id = post_id LIMIT 1;

    if existing_like:
        existing_like.delete() # DELETE FROM like WHERE user_id = user_id AND post_id = post_id;
    else:
        Like.objects.create(user=user, post=post) # INSERT INTO like (user_id, post_id) VALUES (user_id, post_id);

    return HttpResponse(str(post.likes.count()))

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

