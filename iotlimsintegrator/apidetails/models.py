from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _

import userauthentication


class ApplicationDetail(models.Model):
    app_detail_id = models.AutoField(primary_key=True, verbose_name="APP Id")
    name = models.CharField(unique=True, max_length=80, verbose_name="Name")
    base_url = models.CharField(max_length=300, verbose_name="Base URL")
    created_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created DateTime'), null=True, blank=True,
        help_text=_('In UTC'))
    created_by = models.ForeignKey(userauthentication.models.User, null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name="Created By")
    history = AuditlogHistoryField()

    class Meta:
        verbose_name = "APP Detail"
        verbose_name_plural = 'APP Detail'

    def __str__(self):
        return str(self.name)


class APIDetail(models.Model):
    TYPE_CHOICES = [
        ('inbound', 'EM API'),
        ('outbound', 'LIMS API'),
        ('connection', 'Create Connection'), ]
    api_detail_id = models.AutoField(primary_key=True, verbose_name="API Id")
    description = models.CharField(blank=True, null=True, max_length=200, verbose_name="Description")
    name = models.CharField(unique=True, max_length=80, verbose_name="Name")
    app_id = models.ForeignKey(ApplicationDetail, on_delete=models.SET_NULL, null=True, verbose_name="App Id")
    end_point_url = models.CharField(max_length=300, verbose_name="End Point")
    type = models.CharField(max_length=40, choices=TYPE_CHOICES, verbose_name="Type")
    success_code = models.IntegerField(default=200, blank=True, null=True, verbose_name="Success Code")
    authorization_property_id = models.CharField(null=True, blank=True, max_length=200,
                                                 verbose_name="Authorization Property Id", default='')
    authorization_keyword = models.CharField(null=True, blank=True, max_length=200,
                                             verbose_name="Authorization Keyword", default='')
    created_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created DateTime'), null=True, blank=True,
        help_text=_('In UTC'))
    created_by = models.ForeignKey(userauthentication.models.User, null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name="Created By")
    processing_script = models.TextField(verbose_name="Processing Script")
    history = AuditlogHistoryField()

    class Meta:
        verbose_name = "API Detail"
        verbose_name_plural = 'API Detail'

    def __str__(self):
        return str(self.name)


class API_Property_Details(models.Model):
    YESNO_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'), ]

    api_property_details_id = models.AutoField(primary_key='true', verbose_name="API Property Details Id")
    api_detail_id = models.ForeignKey(APIDetail, on_delete=models.CASCADE, null=True, verbose_name="API Detail Id")
    property_id = models.CharField(max_length=80, verbose_name="Property Id", default='')
    property_value = models.CharField(null=True, blank=True, max_length=200, verbose_name="Property Value")
    is_keyword = models.CharField(null=True, blank=True, max_length=40, choices=YESNO_CHOICES,
                                  verbose_name="Is Keyword")
    is_url_property = models.CharField(null=True, blank=True, max_length=40, choices=YESNO_CHOICES,
                                       verbose_name="Is URL Property")
    history = AuditlogHistoryField()

    class Meta:
        verbose_name = "API Property Detail"
        verbose_name_plural = 'API Property Detail'
        unique_together = ('api_detail_id', 'property_id')

    def __str__(self):
        return str(self.property_id)


auditlog.register(ApplicationDetail)
auditlog.register(APIDetail)
auditlog.register(API_Property_Details)
