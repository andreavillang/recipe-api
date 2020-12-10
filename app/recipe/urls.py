from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

# DefaultRouter is from DjangoRest that generates the urls for our view
router = DefaultRouter()
# handles all possible urls related to the viewset. 
# In this case its Tags. an exmaple of this would be 
# /api/recipe/tags → which would retrieve alot of tags
# /api/recipe/tags/1 → which retrieves a specific tag
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]