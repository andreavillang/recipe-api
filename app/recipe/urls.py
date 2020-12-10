from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

# DefaultRouter is from DjangoRest that generates the urls for our view
router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]