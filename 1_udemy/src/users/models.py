from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible

@deconstructible
class GenerateprofileImages(object):
    def __init__(self):
        pass

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f"{instance.user.username}.{ext}"
        return f"profile_images/{filename}"
    
profile_image_path = GenerateprofileImages()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to=profile_image_path, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"