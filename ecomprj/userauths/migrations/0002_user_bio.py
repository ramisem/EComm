# Generated by Django 4.2.7 on 2023-11-13 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(max_length=100, null=True),
        ),
    ]