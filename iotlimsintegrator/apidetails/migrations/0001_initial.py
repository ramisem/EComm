# Generated by Django 4.2.7 on 2024-04-10 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HTTP_Method',
            fields=[
                ('method_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Method Id')),
                ('description', models.CharField(max_length=200, verbose_name='Description')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='Method Name')),
            ],
            options={
                'verbose_name': 'HTTP Method',
                'verbose_name_plural': 'HTTP Method',
            },
        ),
        migrations.CreateModel(
            name='APIDetail',
            fields=[
                ('api_detail_id', models.AutoField(primary_key=True, serialize=False, verbose_name='API Id')),
                ('description', models.CharField(max_length=200, verbose_name='Description')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='Name')),
                ('end_point_url', models.CharField(max_length=300, verbose_name='End Point URL')),
                ('http_method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apidetails.http_method', verbose_name='HTTP Method')),
            ],
            options={
                'verbose_name': 'API Detail',
                'verbose_name_plural': 'API Detail',
            },
        ),
    ]
