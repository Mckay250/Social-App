from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class UserPost(BaseModel):
    user = models.ForeignKey(
        User, verbose_name="Created By", on_delete=models.CASCADE, related_name="posts"
    )
    text = models.TextField()

    def __str__(self) -> str:
        return f"{self.user}'s Post on {self.created_at}"

    class Meta:
        """Metadata."""

        ordering = ["-created_at"]


class Like(BaseModel):
    """A like on a user's post"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user} Like"

    class Meta:
        """Metadata."""

        unique_together = (("user", "post"),)
        ordering = ["-created_at"]


class GeoLocationData(BaseModel):
    """Storing a User's geolocation data"""

    city = models.CharField(max_length=50, null=True)
    region = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    country_code = models.CharField(max_length=5, null=False)
    continent = models.CharField(max_length=24, null=True)
    continent_code = models.CharField(max_length=5, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    user = models.OneToOneField(
        User, unique=True, on_delete=models.CASCADE, related_name="location"
    )

    def __str__(self):
        return f"{self.user}'s location at sign-up was {self.city}"

    class Meta:
        """Metadata."""

        ordering = ["-created_at"]


class UserHolidayData(BaseModel):
    """Storing holiday data from the same day and country the client registered from"""

    name = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    date = models.CharField(max_length=20)
    week_day = models.CharField(max_length=15)
    user = models.OneToOneField(
        User, unique=True, on_delete=models.CASCADE, related_name="holiday"
    )

    def __str__(self):
        return f"It was {self.name} when {self.user} registered"

    class Meta:
        """Metadata."""

        ordering = ["-created_at"]
