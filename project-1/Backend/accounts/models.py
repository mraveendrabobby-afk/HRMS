from django.db import models
from django.contrib.auth.models import User

def upload_to(instance, filename):
    return f'profile_photos/{instance.user.username}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    profile_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    photo = models.ImageField(upload_to=upload_to, blank=True, null=True)

    def __str__(self):
        return self.username or self.user.username
