# Generated by Django 4.1.7 on 2023-04-05 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_user_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
