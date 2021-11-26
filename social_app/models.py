from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Metadata."""
        
        abstract = True

class User(BaseModel, AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    username = None
    ip_address = models.GenericIPAddressField(null=True)
    password = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserPost(BaseModel, models.Model):
    user = models.ForeignKey(User, verbose_name='Created By', on_delete=models.CASCADE, related_name='posts')
    text = models.TextField()

    def __str__(self) -> str:
        return f"{self.user}'s Post on {self.created_at}"

    class Meta:
        """Metadata."""

        ordering = ["-created_at"]
    

class Like(BaseModel):
    """A like on a user's post"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='posts')
    
    def __str__(self):
        return f"{self.user} Like"

    class Meta:
        """Metadata."""

        unique_together = (("user", "post"),)
        ordering = ["-created_at"]

