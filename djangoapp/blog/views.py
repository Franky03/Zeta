from typing import Any
from blog.models import Post, Comment, Like, User
from blog.forms import CommentForm, PostForm
from django.db.models import Q
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormView,CreateView
from django.views import View

from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy



def handler404(request, template_name="blog/pages/404.html"):
    response = render(template_name)
    response.status_code = 404
    return response


@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        if content.strip():
            post = Post.objects.create(author=request.user, content=content)
            
            messages.success(request, 'Post publicado!')
            return redirect('blog:index')
        else:
            return redirect('blog:index')
        
@login_required
def update_post_pre(request, pid):
    print("Post Id: ", pid)
    post = get_object_or_404(Post, id=pid)
    return render(request, 'blog/partials/_update_post.html', {'existing_content': post.content, 'post_id': pid})

@login_required
def update_post_pos(request):
    pid = request.POST.get('pid', '')
    post = get_object_or_404(Post, id=pid)
    if request.method == 'POST':
        new_content = request.POST.get('content', '').strip()

        # Verifica se o conteúdo é vazio
        if not new_content:
            messages.error(request, "O conteúdo do post não pode ser vazio.")
            return render(request, 'blog/partials/_post_card.html', {'post': post})

        # Verifica se o conteúdo não mudou
        if new_content == post.content:
            return render(request, 'blog/partials/_post_card.html', {'post': post})

        # Se o conteúdo é válido e mudou, salva as alterações
        post.content = new_content
        post.save()

        return render(request, 'blog/partials/_post_card.html', {'post': post})
    
@login_required
def update_comment_pre(request, cpk):
    comment = get_object_or_404(Comment, pk=cpk)
    return render(request, 'blog/partials/_update_comment.html', {'existing_content': comment.content, 'comment_pk': cpk})

@login_required
def update_comment_pos(request):
    cpk = request.POST.get('cpk', '')
    comment = get_object_or_404(Comment, pk=cpk)
    if request.method == 'POST':
        new_content = request.POST.get('content', '').strip()

        # Verifica se o conteúdo é vazio
        if not new_content:
            messages.error(request, "O conteúdo do comentário não pode ser vazio.")
            return render(request, 'blog/partials/_comment_card.html', {'comment': comment})

        # Verifica se o conteúdo não mudou
        if new_content == comment.content:
            return render(request, 'blog/partials/_comment_card.html', {'comment': comment})

        # Se o conteúdo é válido e mudou, salva as alterações
        comment.content = new_content
        comment.save()

        return render(request, 'blog/partials/_comment_card.html', {'comment': comment})

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
 
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Define o usuário como autor do post
        response = super().form_valid(form)
        messages.success(self.request, 'Post publicado!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'O conteúdo do post não pode estar vazio.')
        return redirect('blog:index')

def repost_page(request, id):
    post = Post.objects.get_posts().filter(id=id).first()
    print(request.path)
    if not post:
        raise Http404()

    return render(request, 'blog/pages/repost.html', {'post': post, 'page_title': "Home / "})

@login_required
def repost(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        pid = request.POST.get('pid', '')
        original_post = Post.objects.filter(id=pid).first()
        
        post = Post.objects.create(author=request.user, content=content, is_repost=True, original_post=original_post)
        
        messages.success(request, 'Repostado')
        return redirect('blog:index')

@login_required
def repost_directly(request, pid):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        original_post = Post.objects.filter(id=pid).first()
        
        post = Post.objects.create(author=request.user, content=content, is_repost=True, original_post=original_post)
        
        messages.success(request, 'Repostado')
        return redirect('blog:index')
    
@login_required
def delete_post(request, pid):
    post = get_object_or_404(Post, id=pid)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "O post foi deletado com sucesso.")
    
    return redirect('blog:index')

@login_required
def delete_comment(request):
    if request.method == 'POST':
        cpk = request.POST.get('cpk', '')
        comment = get_object_or_404(Comment, pk=cpk)
        comment.delete()
        messages.success(request, "O comentário foi deletado com sucesso.")
    
    return redirect('blog:post', id=comment.post.id)


class CreateCommentView(LoginRequiredMixin, FormView):
    form_class = CommentForm

    def form_valid(self, form):
        content = form.cleaned_data['content']
        post_id = int(self.request.POST.get('pid', ''))
        post = get_object_or_404(Post, id=post_id)

        Comment.objects.create(author=self.request.user, post=post, content=content)
        messages.success(self.request, 'Comentário publicado!')

        return redirect('blog:post', id=post_id)

    def form_invalid(self, form):
        post_id = int(self.request.POST.get('pid', ''))
        messages.error(self.request, 'O conteúdo do comentário não pode estar vazio.')
        return redirect('blog:post', id=post_id)
        
class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id) # SELECT * FROM post WHERE id = post_id;
        user = request.user

        existing_like = Like.objects.filter(user=user, post=post).first() # SELECT * FROM like WHERE user_id = user_id AND post_id = post_id LIMIT 1;

        if existing_like:
            existing_like.delete() # DELETE FROM like WHERE user_id = user_id AND post_id = post_id;
        else:
            Like.objects.create(user=user, post=post) # INSERT INTO like (user_id, post_id) VALUES (user_id, post_id);

        return HttpResponse(str(post.likes.count()), content_type="text/plain")
    
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

class SearchListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        search_value = self.request.GET.get('search', '').strip()
        return Post.objects.get_posts().filter(
            Q(content__icontains=search_value)
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search', '').strip()
        context['search_value'] = search_value
        context['page_title'] = f"{search_value} — Search / "
        return context