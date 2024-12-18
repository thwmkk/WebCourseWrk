from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from characters.models import Character, Media, Episode, Author, MediaType, Group, OffArt, UserMine
from characters.serializers import CharacterSerializer, MediaCreateSerializer, MediaSerializer, EpisodeSerializer, AuthorSerializer, GroupSerializer, MediaTypeSerializer, OffArtSerializer, UserMineSerializer
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.db.models import Func, IntegerField, Count, Max, Min, Avg, Case, When, Value
from django.db.models import F, Func, IntegerField
from django.db.models.functions import Cast
from django.db.models.functions import ExtractYear

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
    # Метод для агрегатной статистики
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Character.objects.aggregate(
            count=Count("id"),
            avg_age=Avg("age"),
            max_age=Max("age"),
            min_age=Min("age"),
        )
        return Response(stats)
      
class MediaViewSet(mixins.CreateModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin, 
                   mixins.DestroyModelMixin, 
                   mixins.ListModelMixin,  
                   GenericViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return MediaCreateSerializer
        return super().get_serializer_class()
      
    def get_queryset(self):
        qs = super().get_queryset()
        # фильтруем по текущему юзеру
        if self.request.user.is_superuser:
            return qs
        else:
            qs = qs.filter(user=self.request.user)
            return qs
  
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Media.objects.aggregate(
            count=Count("id"),
            avg_release_year=Avg(
                Case(
                    When(release_year__isnull=True, then=Value(None)),
                    When(release_year__regex=r'^\d{4}-\d{2}-\d{2}$', then=ExtractYear("release_year")),
                    default=Value(None),
                    output_field=IntegerField()
                )
            ),
            max_release_year=Max(
                Case(
                    When(release_year__isnull=True, then=Value(None)),
                    When(release_year__regex=r'^\d{4}-\d{2}-\d{2}$', then=ExtractYear("release_year")),
                    default=Value(None),
                    output_field=IntegerField()
                )
            ),
            min_release_year=Min(
                Case(
                    When(release_year__isnull=True, then=Value(None)),
                    When(release_year__regex=r'^\d{4}-\d{2}-\d{2}$', then=ExtractYear("release_year")),
                    default=Value(None),
                    output_field=IntegerField()
                )
            ),
        )
        return Response(stats)
        

# API представления для эпизодов
class EpisodeViewSet(mixins.CreateModelMixin, 
  mixins.RetrieveModelMixin, 
  mixins.UpdateModelMixin, 
  mixins.DestroyModelMixin, 
  mixins.ListModelMixin,  
  GenericViewSet ):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Episode.objects.aggregate(
            count=Count("id"),
            avg_number=Avg("number"),
            max_number=Max("number"),
            min_number=Min("number"),
        )
        return Response(stats)
from django.http import HttpResponse
import datetime
from django.db.models import Count, Max, Min, F, ExpressionWrapper, DateField, Sum
class AuthorViewSet(mixins.CreateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    mixins.ListModelMixin,  
                    GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        # Получаем статистику
        stats = Author.objects.aggregate(
            count=Count("id"),
            oldest_author=Max("birth_date"),
            youngest_author=Min("birth_date"),
        )

        # Преобразуем даты в формат YYYY-MM-DD
        if stats['oldest_author']:
            stats['oldest_author'] = stats['oldest_author'].strftime('%Y-%m-%d')
        if stats['youngest_author']:
            stats['youngest_author'] = stats['youngest_author'].strftime('%Y-%m-%d')

        # Получаем самого старого и самого молодого автора
        oldest_author = Author.objects.filter(birth_date=stats['oldest_author']).first()
        youngest_author = Author.objects.filter(birth_date=stats['youngest_author']).first()

        # Подготовка информации о самых старом и молодом авторах
        authors_info = []

        today = datetime.date.today()
        if oldest_author:
            age_oldest = today.year - oldest_author.birth_date.year - ((today.month, today.day) < (oldest_author.birth_date.month, oldest_author.birth_date.day))
            authors_info.append({
                'name': oldest_author.name,
                'birth_date': oldest_author.birth_date.strftime('%Y-%m-%d'),
                'age': age_oldest
            })

        if youngest_author:
            age_youngest = today.year - youngest_author.birth_date.year - ((today.month, today.day) < (youngest_author.birth_date.month, youngest_author.birth_date.day))
            authors_info.append({
                'name': youngest_author.name,
                'birth_date': youngest_author.birth_date.strftime('%Y-%m-%d'),
                'age': age_youngest
            })

        # Формируем HTML-ответ
        response_html = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Статистика авторов</title>
        </head>
        <body>
            <h3>Статистика авторов</h3>
            <p>Количество: {stats['count']}</p>
            <p>Самый старый автор: {authors_info[0]['name']} ({authors_info[0]['birth_date']}, {authors_info[0]['age']} лет)</p>
            <p>Самый молодой автор: {authors_info[1]['name']} ({authors_info[1]['birth_date']}, {authors_info[1]['age']} лет)</p>
        </body>
        </html>
        """

        return HttpResponse(response_html)

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
      
class UserMineViewset(
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.DestroyModelMixin, 
    mixins.ListModelMixin,  
    GenericViewSet):
      queryset = User.objects.all()
      serializer_class = UserMineSerializer
      
      # Новый метод для получения списка пользователей
      def list(self, request, *args, **kwargs):
          if not request.user.is_superuser:
              return Response({"error": "Недостаточно прав доступа."}, status=403)
          
          queryset = self.get_queryset()
          serializer = self.get_serializer(queryset, many=True)
          return Response(serializer.data)
      
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
              return Response({"success": True})
          return Response({"success": False, "error": "Invalid credentials"}, status=400)


      @action(url_path="logout", methods=["GET"], detail=False)
      def logout(self, request, *args, **kwargs):
          logout(request)
          return Response({"success": True})
