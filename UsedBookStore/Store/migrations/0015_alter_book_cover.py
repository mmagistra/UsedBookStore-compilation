# Generated by Django 5.1.4 on 2024-12-18 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0014_alter_book_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='covers/'),
        ),
    ]
