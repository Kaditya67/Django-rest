from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    fields = ('id', 'user', 'image')
    readonly_fields = ('id','user')

admin.site.register(Profile, ProfileAdmin)