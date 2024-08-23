from django.shortcuts import render
from blog.models import Post

# Create your views here.
def index(request):
    posts = Post.objects.get_posts()
    # SELECT * FROM posts ORDER BY created_at DESC 

    return render(request, 'blog/pages/index.html', {'posts': posts})

def page(request):
    return render(request, 'blog/pages/page.html')  

def post(request, id):
    post = Post.objects.get_posts().filter(id=id).first()
    return render(request, 'blog/pages/post.html', {'post': post})