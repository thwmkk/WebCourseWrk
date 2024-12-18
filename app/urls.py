from django.conf import settings
from django.contrib import admin
from django.urls import path, include  # Импортируйте include
from characters.api import CharactersViewset, MediaViewSet, EpisodeViewSet, AuthorViewSet, MediaTypeViewSet, GroupViewSet, OffArtViewset, UserViewset
from rest_framework.routers import DefaultRouter  # Убедитесь, что вы импортируете из правильного модуля
from django.conf.urls.static import static
from characters.views import get_users

router = DefaultRouter()
router.register("characters", CharactersViewset, basename="characters")
router.register("media", MediaViewSet, basename="media")
router.register("episodes", EpisodeViewSet, basename="episodes")
router.register("authors", AuthorViewSet, basename="authors")
router.register("media-types", MediaTypeViewSet, basename="media-types")
router.register("groups", GroupViewSet, basename="groups")
router.register("off-arts", OffArtViewset, basename="offarts")
router.register("users", UserViewset, basename="user")
from characters import views

urlpatterns = [
    path('', views.ShowCharactersView.as_view(), name='show_characters'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Теперь include будет работать
    path('api/users/', get_users, name='get_users'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
