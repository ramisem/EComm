# Generated by Django 4.2.7 on 2024-05-14 12:48

from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IOT_Type',
            fields=[
                ('iot_type_id', models.AutoField(primary_key=True, serialize=False, verbose_name='IOT_Type_Id')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Description')),
                ('model_name', models.CharField(max_length=40, unique=True, verbose_name='IOT Type Name')),
                ('model_id', models.CharField(max_length=40, unique=True, verbose_name='IOT Type')),
            ],
            options={
                'verbose_name': 'IOT Type',
                'verbose_name_plural': 'IOT Types',
            },
        ),
        migrations.CreateModel(
            name='IOT_Device',
            fields=[
                ('iot_device_id', models.AutoField(primary_key=True, serialize=False, verbose_name='IOT_Device_Id')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('serialnumber', models.CharField(max_length=40, verbose_name='Serial #')),
                ('externalid', models.CharField(max_length=80, verbose_name='External Id')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Description')),
                ('manufacturer', models.CharField(blank=True, max_length=200, null=True, verbose_name='Manufacturer')),
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=40, max_length=40, prefix='', unique=True, verbose_name='UUId')),
                ('iot_type_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.iot_type', verbose_name='Type')),
            ],
            options={
                'verbose_name': 'IOT Device',
                'verbose_name_plural': 'IOT Devices',
            },
        ),
    ]
