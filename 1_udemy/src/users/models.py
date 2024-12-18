import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
from house.models import House

@deconstructible
class GenerateprofileImages(object):
    def __init__(self):
        pass

    def __call__(self, instance, filename):
        ext = os.path.splitext(filename)[-1]
        filename = f"{instance.user.username}{ext}"
        return os.path.join('profile_images', filename)

profile_image_path = GenerateprofileImages()  # Instance of the path generator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to=profile_image_path, null=True, blank=True)
    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    def __str__(self):
        return f"{self.user.username}'s Profile"
