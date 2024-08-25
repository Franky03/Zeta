from django.contrib import admin
from blog.models import Tag, Category, Post, Comment, Like, User
from django_summernote.admin import SummernoteModelAdmin
from django.urls import reverse

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1 

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = 'id', 'username', 'email','date_joined'
    list_display_links = 'username',
    search_fields = 'id', 'username', 'email',
    list_per_page = 10
    ordering = '-id',
    list_filter = 'is_staff', 'is_active', 'is_trusty'
    readonly_fields = 'date_joined',
    actions = ['make_trusty', 'make_untrusty']

    def make_trusty(self, request, queryset):
        queryset.update(is_trusty=True)
        self.message_user(request, 'Usuários marcados como confiáveis com sucesso!')

    make_trusty.short_description = 'Marcar como confiável'

    def make_untrusty(self, request, queryset):
        queryset.update(is_trusty=False)
        self.message_user(request, 'Usuários desmarcados como confiáveis com sucesso!')

    make_untrusty.short_description = 'Desmarcar como confiável'
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('name',),
    }

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('name',),
    }

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    inlines = [CommentInline]
    summernote_fields = ('content',)
    list_display = ('id', 'author', 'content', 'created_at', 'updated_at', 'is_repost', 'original_post')
    search_fields = ('content', 'author__username')
    list_display_links = ('content',)
    list_filter = ('created_at', 'is_repost')
    readonly_fields = ('created_at', 'updated_at', 'respost_count')
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('author', 'post', 'content', 'created_at')
    search_fields = ('content', 'author__username', 'post__content')
    list_filter = ('created_at', 'post')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    search_fields = ('user__username', 'post__content')
    list_filter = ('user', 'post')