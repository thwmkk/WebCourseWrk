from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from characters.models import Media, Episode, Character, Author, MediaType, Group

class MediaViewSetTestCase(APITestCase):
    def setUp(self):
        self.media_type = MediaType.objects.create(name="фильм")
        self.author = Author.objects.create(name="Автор 1", birth_date="2000-01-01", description="Описание автора")
        self.media = Media.objects.create(title="Медиа 1", release_year="2022-01-01", description="Описание медиа", media_type=self.media_type, author=self.author)
        self.url = reverse('media-list')

    def test_get_media_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_media(self):
        data = {
            "title": "Новая медиа",
            "release_year": "2023-01-01",
            "description": "Новое описание",
            "media_type": self.media_type.id,
            "author": self.author.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Media.objects.count(), 2)

    def test_update_media(self):
        data = {
            "title": "Обновленная медиа",
            "release_year": "2023-01-01",
            "description": "Обновленное описание",
            "media_type": self.media_type.id,
            "author": self.author.id,
        }
        response = self.client.put(reverse('media-detail', args=[self.media.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.media.refresh_from_db()
        self.assertEqual(self.media.title, "Обновленная медиа")

    def test_delete_media(self):
        response = self.client.delete(reverse('media-detail', args=[self.media.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Media.objects.count(), 0)


class EpisodeViewSetTestCase(APITestCase):
    def setUp(self):
        self.media_type = MediaType.objects.create(name="Аниме")
        self.author = Author.objects.create(name="Автор 1", birth_date="2000-01-01", description="Описание автора")
        self.media = Media.objects.create(title="Медиа 1", release_year="2022-01-01", description="Описание медиа", media_type=self.media_type, author=self.author)
        self.episode = Episode.objects.create(title="Эпизод 1", number=1, description="Описание эпизода", release_date="2022-01-01", media=self.media)
        self.url = reverse('episodes-list')

    def test_get_episode_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_episode(self):
        data = {
            "title": "Новый эпизод",
            "number": 2,
            "description": "Новое описание эпизода",
            "release_date": "2023-01-01",
            "media": self.media.id,  
    }
        response = self.client.post(self.url, data, format='json')

    # Отладочная информация
        print(response.content)  # Выводим содержимое ответа для диагностики

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Episode.objects.count(), 2)


    def test_update_episode(self):
        data = {
            "title": "Обновленный эпизод",
            "number": 1,
            "description": "Обновленное описание",
            "release_date": "2023-01-01",
            "media": self.media.id,
        }
        response = self.client.put(reverse('episodes-detail', args=[self.episode.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.episode.refresh_from_db()
        self.assertEqual(self.episode.title, "Обновленный эпизод")

    def test_delete_episode(self):
        response = self.client.delete(reverse('episodes-detail', args=[self.episode.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Episode.objects.count(), 0)


class CharacterViewSetTestCase(APITestCase):
    def setUp(self):
        self.group = Group.objects.create(name="человек")
        self.media_type = MediaType.objects.create(name="фильм")
        self.character = Character.objects.create(
            name="Каору Нагиса",
            age="15",
            group=self.group,
            description="Описание персонажа",
            media_type=self.media_type
        )
        self.url = reverse('characters-list')

    def test_get_character_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_character(self):
        data = {
            "name": "Новый Персонаж",
            "age": "20",
            "group": self.group.id,
            "description": "Новое описание",
            "media_type": self.media_type.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Character.objects.count(), 2)

    def test_update_character(self):
        data = {
            "name": "Обновленный Персонаж",
            "age": "25",
            "group": self.group.id,
            "description": "Обновленное описание",
            "media_type": self.media_type.id,
        }
        response = self.client.put(reverse('characters-detail', args=[self.character.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.character.refresh_from_db()
        self.assertEqual(self.character.name, "Обновленный Персонаж")

    def test_delete_character(self):
        response = self.client.delete(reverse('characters-detail', args=[self.character.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Character.objects.count(), 0)

class AuthorViewSetTestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Автор 1", birth_date="2000-01-01", description="Описание автора")
        self.url = reverse('authors-list')

    def test_get_author_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_author(self):
        data = {
            "name": "Новый Автор",
            "birth_date": "1995-01-01",
            "description": "Новое описание автора",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_update_author(self):
        data = {
            "name": "Обновленный Автор",
            "birth_date": "1990-01-01",
            "description": "Обновленное описание",
        }
        response = self.client.put(reverse('authors-detail', args=[self.author.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.name, "Обновленный Автор")

    def test_delete_author(self):
        response = self.client.delete(reverse('authors-detail', args=[self.author.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)


class MediaTypeViewSetTestCase(APITestCase):
    def setUp(self):
        self.media_type = MediaType.objects.create(name="фильм")
        self.url = reverse('media-types-list')

    def test_get_media_type_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_media_type(self):
        data = {
            "name": "Новый Тип",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MediaType.objects.count(), 2)

    def test_update_media_type(self):
        data = {
            "name": "Обновленный Тип",
        }
        response = self.client.put(reverse('media-types-detail', args=[self.media_type.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.media_type.refresh_from_db()
        self.assertEqual(self.media_type.name, "Обновленный Тип")

    def test_delete_media_type(self):
        response = self.client.delete(reverse('media-types-detail', args=[self.media_type.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MediaType.objects.count(), 0)
