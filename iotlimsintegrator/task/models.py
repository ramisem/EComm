from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import PeriodicTask

import eventmanagement.models
import userauthentication


class CustomPeriodicTask(PeriodicTask):
    event_rule_id = models.ForeignKey(eventmanagement.models.Event_Rule, on_delete=models.CASCADE,
                                      verbose_name="Event Rule")
    created_by = models.ForeignKey(userauthentication.models.User, null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name="Created By")
    history = AuditlogHistoryField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Periodic Task"
        verbose_name_plural = 'Periodic Tasks'


class TaskAudit(models.Model):
    task_audit_id = models.AutoField(primary_key=True, verbose_name="Task Audit Id")
    name = models.CharField(
        max_length=200,
        verbose_name=_('Task Id'),
        help_text=_('Short Description For This Task'),
        default=''
    )
    uuid = models.CharField(
        max_length=200,
        verbose_name=_('IOT Device Id'),
        default=''
    )
    task_id = models.CharField(
        max_length=getattr(
            settings,
            'DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH',
            255
        ),
        verbose_name=_('Thread ID'),
        help_text=_('Thread ID for the Task that was run'))
    api_url = models.CharField(
        max_length=400,
        verbose_name=_('EM API URL'),
        help_text=_('EM API URL'), default='')
    status = models.CharField(
        max_length=50,
        verbose_name=_('EM API Call Status'),
        help_text=_('EM API Call Status'))
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created DateTime'),
        help_text=_('In UTC'))
    response_text = models.JSONField()
    data_consumed_by_api = models.IntegerField(null=True, blank=True, verbose_name=_('Data Consumed by EM API call'),
                                               help_text=_('In Bytes'))
    condition_evaluation = models.JSONField(default='')
    lims_connection_api_url = models.CharField(
        max_length=400,
        verbose_name=_('LIMS Connection API URL'),
        help_text=_('LIMS Connection API URL'), default='')
    lims_connection_api_status = models.CharField(
        max_length=50,
        verbose_name=_('LIMS Connection API Status'),
        help_text=_('LIMS Connection API Status'), default='')
    lims_connection_api_call_param = models.JSONField(verbose_name=_('LIMS Connection API Call Param'), default='')
    lims_connection_api_response_text = models.JSONField(verbose_name=_('LIMS Connection API Call Response'),
                                                         default='')
    data_consumed_by_lims_connection_api = models.IntegerField(null=True, blank=True,
                                                               verbose_name=_(
                                                                   'Data Consumed by LIMS Connection API call'),
                                                               help_text=_('In Bytes'))
    lims_api_url = models.CharField(
        max_length=400,
        verbose_name=_('LIMS API URL'),
        help_text=_('LIMS API URL'), default='')
    lims_status = models.CharField(
        max_length=50,
        verbose_name=_('LIMS API Status'),
        help_text=_('LIMS API Status'), default='')
    lims_api_call_param = models.JSONField(verbose_name=_('LIMS API Call Param'), default='')
    lims_response_text = models.JSONField(verbose_name=_('LIMS API Call Response'), default='')
    data_consumed_by_lims_api = models.IntegerField(null=True, blank=True,
                                                    verbose_name=_('Data Consumed by LIMS API call'),
                                                    help_text=_('In Bytes'))
    total_data_consumed = models.IntegerField(null=True, blank=True,
                                              verbose_name=_('Total Data Consumed'),
                                              help_text=_('In Bytes'))

    class Meta:
        verbose_name = "Task Audit"
        verbose_name_plural = 'Task Audit'


auditlog.register(CustomPeriodicTask)
