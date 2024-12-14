from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) 


@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    if not instance.username: 
        username = f"{instance.first_name}_{instance.last_name}".lower()
        if not username:   
            username = "user"
 
        counter = 0
        unique_username = username
        while User.objects.filter(username=unique_username).exists():
            counter += 1
            unique_username = f"{username}_{counter}"
        instance.username = unique_username