# Generated by Django 3.0.8 on 2020-07-27 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_like_post_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followee',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='followee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='follower',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
