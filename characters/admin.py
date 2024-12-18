from django.contrib import admin
from .models import Group, Character, Media, Episode, Author, OffArt, MediaType

# Регистрация модели Character
@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age']

# Регистрация модели Group
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

# Регистрация модели Media
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'release_year', 'description', 'media_type', 'author']

# Регистрация модели Episode
@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'number', 'release_date', 'media']

# Регистрация модели Author
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'birth_date', 'description']

# Регистрация модели OffArt
@admin.register(OffArt)
class OffArtAdmin(admin.ModelAdmin):
    list_display = ['id', 'media']

# Регистрация модели MediaType
@admin.register(MediaType)
class MediaTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
