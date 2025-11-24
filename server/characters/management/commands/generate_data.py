import random
from faker import Faker
from django.core.management.base import BaseCommand
from characters.models import Character, Group, Author, MediaType, Media, Episode

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        
        # Получаем все группы из базы данных
        groups = Group.objects.all()
        media_types = MediaType.objects.all()
        authors = Author.objects.all()

        for _ in range(1000):
            # Случайный выбор группы и медиа типа
            random_group = random.choice(groups) if groups else None
            random_media_type = random.choice(media_types) if media_types else None
            random_author = random.choice(authors) if authors else None

            # Создание персонажа
            Character.objects.create(
                name=fake.name(),
                age=fake.random_int(min=1, max=100),
                media_type=random_media_type,
                description=fake.text(),
                group=random_group
            )

            # Создание автора
            Author.objects.create(
                name=fake.name(),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=90),
                description=fake.text()
            )
            
            Media.objects.create(
                title=fake.sentence(nb_words=3),
                release_year=fake.date(),
                description=fake.text(),
                media_type=random_media_type,
                author=random_author
            )
            
            # Создание медиа
            media = Media.objects.create(
                title=fake.sentence(nb_words=3),
                release_year=fake.date(),
                description=fake.text(),
                media_type=random_media_type,
                author=random_author
            )

            # Создание эпизода
            Episode.objects.create(
                title=fake.sentence(nb_words=3),
                number=fake.random_int(min=1, max=20),
                description=fake.text(),
                release_date=fake.date(),
                media=media
            )
