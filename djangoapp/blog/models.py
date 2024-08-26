from django.db import models
from django.contrib.auth.models import UserManager,AbstractBaseUser, PermissionsMixin, Group, Permission
from utils.rands import slugify_new
from django_summernote.models import AbstractAttachment
from utils.images import resize_image
from django.urls import reverse
from django import forms
from django_summernote.widgets import SummernoteWidget
from django.conf import settings
from django.core import validators
import re
from django.utils import timezone

# Create your models here.

class UserManager(UserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
          raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                 is_staff=is_staff, is_active=True,
                 is_superuser=is_superuser, last_login=now,
                 date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user=self._create_user(username, email, password, True, True,
                 **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField('username', max_length=15, unique=True)
    help_text='Required. 15 characters or fewer. Letters, numbers and @/./+/-/_ characters',
    validators=[validators.RegexValidator(re.compile(r'^[\w.@+-]+$'),'Enter a valid username.','invalid')]
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=30)
    email = models.EmailField('email address', max_length=255, unique=True)
    is_staff = models.BooleanField('staff status', default=False,
    help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField('active', default=True,help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    is_trusty = models.BooleanField('trusty', default=False, help_text='Designates whether this user has confirmed his account.')

    groups = models.ManyToManyField(Group, related_name='blog_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='blog_user_set', blank=True)

    bio = models.TextField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', default=0, blank=True)
    # symmetrical=False, significa que a relação não é simétrica, ou seja, se eu sigo você, você não me segue automaticamente e vice-versa
    # related_name='followers', é o nome que eu vou usar para acessar os seguidores de um usuário

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    """ def get_absolute_url(self):
        return reverse('blog:profile', args=[self.username,]) """
    

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
            if self.content != '' and self.content != self.original_post.content:
                self.content = (
                    f'<div class="new-post-content">{self.content}</div>'
                    f'<div class="old-post-content">{self.original_post.content}</div>'
                )
            else:
                self.content = self.original_post.content

        return super().save(*args, **kwargs)
    
    def like_count(self):
        return self.likes.count() if self.likes else 0
    
    def reposts_count(self):
        return self.reposts.count() if self.reposts else 0
    
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'post')  # Garante que um usuário não pode curtir o mesmo post mais de uma vez

    def __str__(self):
        return f'{self.user.username} likes {self.post.content[:30]}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
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

