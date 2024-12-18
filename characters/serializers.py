from rest_framework import serializers
from characters.models import Media, Episode, Character, Group, Author, MediaType, OffArt

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class CharacterSerializer(serializers.ModelSerializer):
    # group = GroupSerializer(read_only=False)
    class Meta:
        model = Character
        fields = ['id', 'name', 'picture', 'age', 'group','description','media_type']

class MediaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaType
        fields = ['id', 'name']
        
class OffArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffArt
        fields = ['id', 'picture', 'media_type'] 

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'birth_date', 'description']

class MediaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'title', 'release_year', 'description', 'media_type', 'author']

class MediaSerializer(serializers.ModelSerializer):
   # author = AuthorSerializer(read_only=True)  # Вложенный сериализатор для автора
    # media_type = MediaTypeSerializer(read_only=True)  # Вложенный сериализатор для типа медиа

    class Meta:
        model = Media
        fields = ['id', 'title', 'release_year', 'description', 'media_type', 'author']

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'title', 'number', 'description', 'release_date', 'media']

    #def validate_media(self, value):
     #   if value.media_type.name != 'Аниме':
      #      raise serializers.ValidationError('Эпизод может быть связан только с аниме.')
       # return value

        