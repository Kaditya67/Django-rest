import os
import uuid
from django.db import models
from django.utils.deconstruct import deconstructible

@deconstructible
class GenerateHouseImagePath(object):
    def __init__(self):
        pass

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.id:
            path = f'houses/{instance.id}/images'
        else:
            path = 'houses/temp/images'  # Temporary path until instance is saved
        name = f'main.{ext}'
        return os.path.join(path, name)

house_image_path = GenerateHouseImagePath()

class House(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to=house_image_path)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    manager = models.OneToOneField('users.Profile', on_delete=models.SET_NULL, null=True, blank=True,related_name="managed_house")
    points = models.IntegerField(default=0)
    completed_tasks_count = models.IntegerField(default=0)
    notcompleted_tasks_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} House'

