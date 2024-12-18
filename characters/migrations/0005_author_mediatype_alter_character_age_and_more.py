# Generated by Django 5.1.1 on 2024-09-18 09:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0004_alter_group_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('birth_date', models.DateField()),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='MediaType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Тип медиа',
                'verbose_name_plural': 'Типы медиа',
            },
        ),
        migrations.AlterField(
            model_name='character',
            name='age',
            field=models.CharField(max_length=10, verbose_name='Возраст'),
        ),
        migrations.AlterField(
            model_name='character',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='characters.group'),
        ),
        migrations.AlterField(
            model_name='character',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('release_year', models.IntegerField()),
                ('description', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.author')),
                ('media_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.mediatype')),
            ],
            options={
                'verbose_name': 'Медиа',
                'verbose_name_plural': 'Медиа',
            },
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('number', models.IntegerField()),
                ('description', models.TextField()),
                ('release_date', models.DateField()),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='characters.media')),
            ],
            options={
                'verbose_name': 'Эпизод',
                'verbose_name_plural': 'Эпизоды',
            },
        ),
        migrations.CreateModel(
            name='OffArt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='off_art/')),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='off_arts', to='characters.media')),
            ],
            options={
                'verbose_name': 'Официальные арты',
                'verbose_name_plural': 'Официальные арты',
            },
        ),
        migrations.AddField(
            model_name='media',
            name='off_art',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='media_items', to='characters.offart'),
        ),
    ]