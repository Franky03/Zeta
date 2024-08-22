from django.db import models
from django.contrib.auth.models import User
from utils.rands import slugify_new
from django_summernote.models import AbstractAttachment
from utils.images import resize_image

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
    
    
class Post(models.Model):
    # quando eu for acessar pelo usuário meus posts, eu quero que ele me retorne todos os posts que eu criei, logo o related_name='posts' é para isso
    # vou buscar de dentro do usuário os post que ele criou, relação inversa
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_repost = models.BooleanField(default=False)
    original_post = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reposts', null=True, blank=True)
    respost_count = models.IntegerField(default=0)
 
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username}: {self.content[:30]}'
    
    def save(self, *args, **kwargs):
        if self.is_repost:
            self.respost_count = self.original_post.reposts.count() + 1

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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}: {self.content[:30]}'
    