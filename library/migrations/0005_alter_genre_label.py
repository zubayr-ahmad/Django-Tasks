# Generated by Django 5.1.7 on 2025-03-21 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_genre_alter_book_author_book_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='label',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
