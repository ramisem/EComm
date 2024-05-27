# Generated by Django 4.2.7 on 2024-05-14 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eventmanagement', '0001_initial'),
        ('masterdata', '0001_initial'),
        ('core', '0001_initial'),
        ('apidetails', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event_rule',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='event_rule',
            name='event_iot_map_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterdata.event_type_iot_type_map', verbose_name='Event_Type_IOT_Type_Map_Id'),
        ),
        migrations.AddField(
            model_name='event_rule',
            name='event_type_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='masterdata.event_type', verbose_name='Event Type'),
        ),
        migrations.AddField(
            model_name='event_rule',
            name='inbound_api',
            field=models.ForeignKey(limit_choices_to={'type': 'inbound'}, on_delete=django.db.models.deletion.CASCADE, related_name='inbound_api_related', to='apidetails.apidetail', verbose_name='EM API'),
        ),
        migrations.AddField(
            model_name='event_rule',
            name='iot_type_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.iot_type', verbose_name='IOT Type'),
        ),
        migrations.AddField(
            model_name='event_rule',
            name='outbound_api',
            field=models.ForeignKey(limit_choices_to={'type': 'outbound'}, on_delete=django.db.models.deletion.CASCADE, related_name='outbound_api_related', to='apidetails.apidetail', verbose_name='LIMS API'),
        ),
        migrations.AlterUniqueTogether(
            name='event_rule_params',
            unique_together={('event_rule_id', 'param_id')},
        ),
    ]