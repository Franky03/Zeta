from django.db import models
from django.contrib.auth.models import User
from utils.rands import slugify_new
from django_summernote.models import AbstractAttachment
from utils.images import resize_image
from django.urls import reverse
from django import forms
from django_summernote.widgets import SummernoteWidget

# Create your models here.

class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name

        if file_changed:
            resize_image(self.file, 900, True, 70)

        return super_save

class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
    
class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    
class PostManager(models.Manager):
    def get_posts(self):
        return self.order_by('-created_at')
    
class Post(models.Model):
    # quando eu for acessar pelo usuário meus posts, eu quero que ele me retorne todos os posts que eu criei, logo o related_name='posts' é para isso
    # vou buscar de dentro do usuário os post que ele criou, relação inversa
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_repost = models.BooleanField(default=False)
    original_post = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reposts', null=True, blank=True) # isso é uma relação recursiva
    respost_count = models.IntegerField(default=0)
 
    class Meta:
        ordering = ['-created_at']

    objects = PostManager()

    def get_absolute_url(self):
        return reverse('blog:post', args=[self.id,])
    

    def __str__(self):
        return f'{self.author.username}: {self.content[:30]}'
    
    def save(self, *args, **kwargs):
        if not self.author:
            # se o autor não for informado, o autor será o usuário logado
            self.author = User.objects.first()

        if self.is_repost:
            self.respost_count = self.original_post.reposts.count() + 1

        # se o post for um repost, o conteúdo do post será o conteúdo do post original
        # mas se o post tiver um conteúdo diferente, o conteúdo do post será o conteúdo do post + o conteúdo do post original

        if self.is_repost:
            if self.content != self.original_post.content:
                self.content = f'{self.content}\n\n{self.original_post.content}'
            else:
                self.content = self.original_post.content

        return super().save(*args, **kwargs)
    
    def like_count(self):
        return self.likes.count() if self.likes else 0
    
    def reposts_count(self):
        return self.reposts.count() if self.reposts else 0
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'post')  # Garante que um usuário não pode curtir o mesmo post mais de uma vez

    def __str__(self):
        return f'{self.user.username} likes {self.post.content[:30]}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.author:
            self.author = User.objects.first()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.author.username}: {self.content[:30]}'

