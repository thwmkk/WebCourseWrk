# Generated by Django 5.1.3 on 2024-12-18 13:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("characters", "0013_media_user"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="User",
            new_name="UserMine",
        ),
    ]
