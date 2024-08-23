from django.shortcuts import render
from blog.models import Post

# Create your views here.
def index(request):
    posts = Post.objects \
        .filter(is_repost=False) \
        .order_by('-created_at') 
    # SELECT * FROM posts WHERE is_repost = False ORDER BY created_at DESC 

    return render(request, 'blog/pages/index.html', {'posts': posts})

def page(request):
    return render(request, 'blog/pages/page.html')  

def post(request):
    return render(request, 'blog/pages/post.html')