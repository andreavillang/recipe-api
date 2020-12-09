from rest_framework import generics, authentication, permissions
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

class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Manage the authenticated user
    """
    # Create a serializer class atribute
    serializer_class = UserSerializer
    # We need authenticate the user, this is done by assigning it a token, you can also use cookie authentication but for this case, we're using token
    authentication_classes = (authentication.TokenAuthentication,)
    # The level of access the user has. In this case we dont need any super admin permission. The user just needs to be logged in/Authenticated
    permission_classes = (permissions.IsAuthenticated,)

    # We are actually overriding the get_object function. Why? Becuase we just want to get the specific logged in user and only that.
    def get_object(self):
        """
        Retrieve and return authentication user
        """
        return self.request.user