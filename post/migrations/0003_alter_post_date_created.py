# Generated by Django 4.0.4 on 2022-05-26 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_created',
            field=models.DateTimeField(auto_now=True, verbose_name='Date Created'),
        ),
    ]