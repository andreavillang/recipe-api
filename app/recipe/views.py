from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag

from recipe import serializers

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
    Manage tags in the database
    """
    
    # This will require the access to have a token
    authentication_classes = (TokenAuthentication,)
    # This will require the access to be from an authenticated user/token
    permission_classes = (IsAuthenticated,)

    # When you define a listed query, you need to have a query set you want to return. In this case I want to return them ALL
    queryset = Tag.objects.all()
    # Assign the serializer we made.
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """
        Return objects based on the user.
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')
