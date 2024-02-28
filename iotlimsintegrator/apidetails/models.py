from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField
from django.db import models


class HTTP_Method(models.Model):
    method_id = models.AutoField(primary_key=True, verbose_name="Method Id")
    description = models.CharField(max_length=200, verbose_name="Description")
    name = models.CharField(unique=True, max_length=80, verbose_name="Method Name")
    history = AuditlogHistoryField()

    class Meta:
        verbose_name = "HTTP Method"
        verbose_name_plural = 'HTTP Method'

    def __str__(self):
        return str(self.name)


class APIDetail(models.Model):
    api_detail_id = models.AutoField(primary_key=True, verbose_name="API Id")
    description = models.CharField(max_length=200, verbose_name="Description")
    name = models.CharField(unique=True, max_length=80, verbose_name="Name")
    http_method = models.ForeignKey(HTTP_Method, on_delete=models.SET_NULL, null=True, verbose_name="HTTP Method")
    end_point_url = models.CharField(max_length=300, verbose_name="End Point URL")
    history = AuditlogHistoryField()

    class Meta:
        verbose_name = "API Detail"
        verbose_name_plural = 'API Detail'

    def __str__(self):
        return str(self.name)


auditlog.register(HTTP_Method)
auditlog.register(APIDetail)
