from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, BlogsDetails, Comment
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'email', 'username', 'get_full_name', 'date_of_birth', 'is_superuser', 'is_role', 'is_reader', 'is_blogger', 'is_active']
    ordering = ['id']

class BlogsDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'blog_title', 'blog_date', 'blog_content', 'created_by']
    ordering = ['id']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment', 'blog_title', 'created_by', 'comment_date']
    ordering = ['id']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(BlogsDetails, BlogsDetailsAdmin)
admin.site.register(Comment, CommentAdmin)




