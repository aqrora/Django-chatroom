# Generated by Django 4.1.7 on 2023-04-12 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_alter_user_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]