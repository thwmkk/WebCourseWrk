from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from characters.models import Character, Media, Episode, Author, MediaType, Group, OffArt
from characters.serializers import CharacterSerializer, MediaCreateSerializer, MediaSerializer, EpisodeSerializer, AuthorSerializer, GroupSerializer, MediaTypeSerializer, OffArtSerializer

class CharactersViewset(
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.DestroyModelMixin, 
    mixins.ListModelMixin,  
    GenericViewSet ):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
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
