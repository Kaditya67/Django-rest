from rest_framework import routers
from .viewsets import UserViewSet, ProfileViewSet

app_name = 'users'
router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('profiles', ProfileViewSet, basename='profile')

# urlpatterns = router.urls