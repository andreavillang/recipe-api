from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from core.models import Tag, Ingredient, Recipe

from recipe import serializers

class BaseViewSetAttr(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
    Base viewsetfor recipe
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Return objects for the current valid user
        """
        return self.queryset.filter(user = self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """
        Creates a new object
        """
        serializer.save(user = self.request.user)

class TagViewSet(BaseViewSetAttr):
    """
    Manage tags in the database
    """
    
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

class IngredientViewSet(BaseViewSetAttr):
    """
    Manage ingredients in the database
    """

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    """
    Manage recipes in the database
    """

    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Retrieve the recipes for the authenticated user
        """

        return self.queryset.filter(user=self.request.user).order_by('-id')
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class
        """

        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new recipe
        """
        # By default, Django already knows how to make the Recipe object. This line of code ties it to the user.
        serializer.save(user=self.request.user)
    
    # @action method allows us to make custom functions aside from the premade 
    # functions that Django Provides.
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """
        Upload an image to a recipe
        """
        # This will always be the way you call to grab the object
        recipe = self.get_object()
        # we grab the recipe and pass in whatever data we got from the request. This also triggers get_serializer_class
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        # is_valid checks if the image is the same asthe imagefield value we assigned
        if serializer.is_valid():
            # Save the valid serializer
            serializer.save()
            # return what we got. Since our serializers return the object. And we also return that since its valid then its an OK
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        # Else, theres an error.
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    