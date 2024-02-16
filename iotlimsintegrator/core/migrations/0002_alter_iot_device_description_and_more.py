# Generated by Django 4.2.7 on 2024-02-13 18:05

from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iot_device',
            name='description',
            field=models.CharField(max_length=200, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='iot_device',
            name='externalid',
            field=models.CharField(max_length=80, verbose_name='External Id'),
        ),
        migrations.AlterField(
            model_name='iot_device',
            name='iot_type_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.iot_type', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='iot_device',
            name='manufacturer',
            field=models.CharField(max_length=200, verbose_name='Manufacturer'),
        ),
        migrations.AlterField(
            model_name='iot_device',
            name='name',
            field=models.CharField(max_length=80, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='iot_device',
            name='serialnumber',
            field=models.CharField(max_length=40, verbose_name='Serial #'),
        ),
        migrations.AlterField(
            model_name='iot_device',
            name='uuid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, length=40, max_length=40, prefix='', unique=True, verbose_name='UUId'),
        ),
        migrations.AlterField(
            model_name='iot_type',
            name='description',
            field=models.CharField(max_length=200, verbose_name='Description'),
        ),
    ]