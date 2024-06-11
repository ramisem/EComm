from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    history = AuditlogHistoryField()

    class Meta:
        verbose_name = "Registered User"
        verbose_name_plural = 'Registered Users'

    def __str__(self):
        return self.username


auditlog.register(User)
