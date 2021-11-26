from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Like, User, UserPost


@admin.register(UserPost)
class UserPostAdmin(admin.ModelAdmin):
    """Admin for posts."""

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Admin for Likes."""