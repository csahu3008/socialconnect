# Generated by Django 4.0.4 on 2022-05-25 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='uploads/', verbose_name='Image'),
        ),
    ]
