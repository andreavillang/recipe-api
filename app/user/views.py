from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """
    Create a new auth token for user
    """
    # Same as what we did in the create user. We have a fucntion and now we need to access this given a URL
    serializer_class = AuthTokenSerializer
    # This one allows us to view the endpoint if we were to make this call in the browser.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES