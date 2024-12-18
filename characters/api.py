from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from characters.models import Character, Media, Episode, Author, MediaType, Group, OffArt
from characters.serializers import CharacterSerializer, MediaCreateSerializer, MediaSerializer, EpisodeSerializer, AuthorSerializer, GroupSerializer, MediaTypeSerializer, OffArtSerializer
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class CharactersViewset(
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.DestroyModelMixin, 
    mixins.ListModelMixin,  
    GenericViewSet ):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    
    def get_queryset(self):
      qs = super().get_queryset()
      # фильтруем по текущему юзеру
      if (self.request.user.is_superuser):
        return qs
      else:
        qs = qs.filter(user=self.request.user)
        return qs

      
      
    # API представления для медиа
class MediaViewSet(mixins.CreateModelMixin, 
  mixins.RetrieveModelMixin, 
  mixins.UpdateModelMixin, 
  mixins.DestroyModelMixin, 
  mixins.ListModelMixin,  
  GenericViewSet ):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return MediaCreateSerializer
        return super().get_serializer_class()
      
    def get_queryset(self):
      qs = super().get_queryset()
      # фильтруем по текущему юзеру
      if (self.request.user.is_superuser):
        return qs
      else:
        qs = qs.filter(user=self.request.user)
        return qs
        

# API представления для эпизодов
class EpisodeViewSet(mixins.CreateModelMixin, 
  mixins.RetrieveModelMixin, 
  mixins.UpdateModelMixin, 
  mixins.DestroyModelMixin, 
  mixins.ListModelMixin,  
  GenericViewSet ):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer

# API представления для авторов
class AuthorViewSet(mixins.CreateModelMixin, 
  mixins.RetrieveModelMixin, 
  mixins.UpdateModelMixin, 
  mixins.DestroyModelMixin, 
  mixins.ListModelMixin,  
  GenericViewSet ):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# API представления для типов медиа
class MediaTypeViewSet(mixins.CreateModelMixin, 
  mixins.RetrieveModelMixin, 
  mixins.UpdateModelMixin, 
  mixins.DestroyModelMixin, 
  mixins.ListModelMixin,  
  GenericViewSet ):
    queryset = MediaType.objects.all()
    serializer_class = MediaTypeSerializer

    # API представления для типов медиа
class GroupViewSet(mixins.CreateModelMixin, 
  mixins.RetrieveModelMixin, 
  mixins.UpdateModelMixin, 
  mixins.DestroyModelMixin, 
  mixins.ListModelMixin,  
  GenericViewSet ):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class OffArtViewset(
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.DestroyModelMixin, 
    mixins.ListModelMixin,  
    GenericViewSet ):
      queryset = OffArt.objects.all()
      serializer_class = OffArtSerializer
      
class UserViewset(GenericViewSet):
    @action(url_path="info", methods=["GET"], detail=False)
    def get_info(self, request, *args, **kwargs):
        data = {
            "is_authenticated": request.user.is_authenticated
        }
        if request.user.is_authenticated:
            data.update({
                "is_superuser": request.user.is_superuser,
                "username": request.user.username,
                "user_id": request.user.id,
            })
        return Response(data)

    @action(url_path="login", methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):
        username = request.data.get("user")
        password = request.data.get("pass")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"success": False, "error": "Invalid credentials"}, status=400)

    @action(url_path="logout", methods=["GET"], detail=False)
    def logout(self, request, *args, **kwargs):
        logout(request)
        return Response({"success": True})
