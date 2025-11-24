from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from .models import Media, Episode, Character, Author, MediaType, UserMine
from .serializers import MediaSerializer, EpisodeSerializer, CharacterSerializer, AuthorSerializer, MediaTypeSerializer, UserMineSerializer
from rest_framework.decorators import api_view
# Обычное представление для отображения персонажей
class ShowCharactersView(View):
    template_name = "characters/show_characters.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = {}
        context['characters'] = Character.objects.all()  # Получение всех персонажей
        return context
