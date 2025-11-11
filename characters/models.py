from django.db import models
from django.core.exceptions import ValidationError

class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self) -> str:
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    age = models.CharField(max_length=10, verbose_name="Возраст")
    picture = models.ImageField("Изображение", null=True, upload_to="characters")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=True, related_name='characters',verbose_name="Группа")
    description = models.TextField(verbose_name="Описание персонажа",default='Описание отсутствует')
    media_type = models.ForeignKey("MediaType", on_delete=models.CASCADE, null=True, related_name='characters_for_media',verbose_name="Откуда")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Пользователь", null=True)
    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    birth_date = models.DateField(verbose_name="Дата рождения")
    description = models.TextField(verbose_name="Биография")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.name


class MediaType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")

    class Meta:
        verbose_name = "Тип медиа"
        verbose_name_plural = "Типы медиа"

    def __str__(self):
        return self.name


class OffArt(models.Model):
    picture = models.ImageField("Арт", null= True, upload_to='off_arts')
    media_type = models.ForeignKey("MediaType", on_delete=models.CASCADE, null=True, related_name='off_arts', verbose_name="Откуда")

    class Meta:
        verbose_name = "Официальные арты"
        verbose_name_plural = "Официальные арты"

    def __str__(self):
        return f"Арты для {self.media_type}"


class Media(models.Model):
    title = models.CharField(max_length=128, verbose_name="Название")
    release_year = models.DateField(verbose_name="Год выпуска")
    description = models.TextField(verbose_name="Описание")
    media_type = models.ForeignKey('MediaType', on_delete=models.CASCADE, verbose_name="Тип медиа")
    author = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name="Автор")  # Не допускает NULL
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Пользователь", null=True)

    class Meta:
        verbose_name = "Медиа"
        verbose_name_plural = "Медиа"

    def __str__(self):
        return self.title


class Episode(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    number = models.IntegerField(verbose_name="Номер серии")
    description = models.TextField(verbose_name="Описание эпизода")
    release_date = models.DateField(verbose_name="Год выпуска")
    media = models.ForeignKey('Media', on_delete=models.CASCADE, related_name='episodes',verbose_name="Тип медиа")

    class Meta:
        verbose_name = "Эпизод"
        verbose_name_plural = "Эпизоды"

    def __str__(self):
        return f"{self.title} (Эпизод {self.number})"

    def clean(self):
        super().clean()
        print(f"Тип медиа: {self.media.media_type.name}")  # Отладочный вывод
        if self.media.media_type.name != 'аниме':
            raise ValidationError('Эпизод может быть связан только с аниме.')
        
class UserMine(models.Model):
  name = models.TextField("Имя")
  surname = models.TextField("Фамилия")


  class Meta:
    verbose_name = "Пользователь"
    verbose_name_plural = "Пользователи"

  def str(self) -> str:
    return self.name

