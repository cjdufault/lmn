# Generated by Django 3.1.2 on 2020-11-15 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmn', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='user_images/'),
        ),
    ]
