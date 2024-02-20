from auditlog.registry import auditlog
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from shortuuid.django_fields import ShortUUIDField
from auditlog.models import AuditlogHistoryField, LogEntry


class IOT_Type(models.Model):
    iot_type_id = models.AutoField(primary_key=True, verbose_name="IOT_Type_Id")
    description = models.CharField(max_length=200, verbose_name="Description")
    history = AuditlogHistoryField()

    class Meta:
        verbose_name = "IOT Type"
        verbose_name_plural = 'IOT Types'

    def __str__(self):
        return str(self.description)


class IOT_Device(models.Model):
    iot_device_id = models.AutoField(primary_key=True, verbose_name="IOT_Device_Id")
    name = models.CharField(max_length=80, verbose_name="Name")
    iot_type_id = models.ForeignKey(IOT_Type, on_delete=models.SET_NULL, null=True, verbose_name="Type")
    serialnumber = models.CharField(max_length=40, verbose_name="Serial #")
    externalid = models.CharField(max_length=80, verbose_name="External Id")
    description = models.CharField(max_length=200, verbose_name="Description")
    manufacturer = models.CharField(max_length=200, verbose_name="Manufacturer")
    uuid = ShortUUIDField(unique=True, length=40, max_length=40, verbose_name="UUId")
    history = AuditlogHistoryField()

    class Meta:
        verbose_name = "IOT Device"
        verbose_name_plural = 'IOT Devices'

    def __str__(self):
        return self.uuid


class ArchivedAuditLogData(models.Model):
    action = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)
    object_id = models.TextField(null=True, blank=True)
    actor_id = models.TextField(null=True, blank=True)
    object_repr = models.TextField()
    remote_addr = models.TextField()
    changes = models.TextField();


@receiver(pre_delete, sender=LogEntry, dispatch_uid='delete_logentry_signal')
def archive_audit_logs(sender, instance, **kwargs):
    print('Pre Delete called')
    archived_log = ArchivedAuditLogData()
    archived_log.action = instance.action
    archived_log.timestamp = instance.timestamp
    archived_log.object_id = instance.object_id
    archived_log.actor_id = instance.actor_id
    archived_log.object_repr = instance.object_repr
    archived_log.remote_addr = instance.remote_addr
    archived_log.changes = instance.changes
    archived_log.save()


auditlog.register(IOT_Type)
auditlog.register(IOT_Device)
