# Generated by Django 4.2.7 on 2024-04-10 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0001_initial'),
        ('eventmanagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event_rule_params',
            name='value_text',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='event_rule',
            name='event_iot_map_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='masterdata.event_type_iot_type_map', verbose_name='Event_Type_IOT_Type_Map_Id'),
        ),
    ]
