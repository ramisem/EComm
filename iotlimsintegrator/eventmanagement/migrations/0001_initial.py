# Generated by Django 4.2.7 on 2024-04-08 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('masterdata', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event_Rule',
            fields=[
                ('event_rule_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Event_RuleID')),
                ('name', models.CharField(max_length=80, null=True, unique=True, verbose_name='Rule Name')),
                ('rule_frequency', models.IntegerField(null=True, verbose_name='Frequency')),
                ('rule_frequency_unit', models.CharField(choices=[('sec', 'SECOND'), ('d', 'DAY'), ('m', 'MONTH'), ('y', 'YEAR')], max_length=40, null=True, verbose_name='Frequency Unit')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('event_iot_map_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='masterdata.event_type_iot_type_map', verbose_name='Event_Type_IOT_Type_Map_Id')),
                ('event_type_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='masterdata.event_type', verbose_name='Event Type')),
                ('iot_type_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.iot_type', verbose_name='IOT Type')),
            ],
            options={
                'verbose_name': 'Event Rule',
                'verbose_name_plural': 'Event Rules',
            },
        ),
        migrations.CreateModel(
            name='Event_Rule_Params',
            fields=[
                ('event_rule_param_ispec_condition_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Event Rule Parameter Id')),
                ('operator1', models.CharField(blank=True, choices=[('=', '='), ('<', '<'), ('<=', '<='), ('>', '>'), ('>=', '>=')], max_length=40, null=True, verbose_name='Operator-1')),
                ('value1', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Value1')),
                ('condition', models.CharField(blank=True, choices=[('and', 'AND'), ('or', 'OR')], max_length=40, null=True, verbose_name='Condition')),
                ('operator2', models.CharField(blank=True, choices=[('=', '='), ('<', '<'), ('<=', '<='), ('>', '>'), ('>=', '>=')], max_length=40, null=True, verbose_name='Operator-2')),
                ('value2', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Value2')),
                ('duration', models.IntegerField(blank=True, null=True, verbose_name='Duration')),
                ('event_rule_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eventmanagement.event_rule', verbose_name='Event Rule Id')),
                ('param_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterdata.param', verbose_name='Parameter ID')),
                ('unit_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterdata.unit', verbose_name='Duration Unit')),
            ],
            options={
                'verbose_name': 'Event Rule Parameter',
                'verbose_name_plural': 'Event Rule Parameters',
                'unique_together': {('event_rule_id', 'param_id')},
            },
        ),
    ]
