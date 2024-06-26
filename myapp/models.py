from django.db import models
from django.utils import timezone
import uuid

now_utc = timezone.now()
# Convert to 'Europe/Paris' timezone
now_paris = now_utc.astimezone(timezone.get_current_timezone())

class SourceModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default='')
    data_vendor = models.CharField(max_length=255, default='')
    panel = models.CharField(max_length=255, default='')
    panel_group = models.CharField(max_length=255, default='DKM')
    scope_of_subscription = models.CharField(max_length=255, default='', blank=True)
    data_type = models.CharField(max_length=255, default='')
    granularity = models.CharField(max_length=255, default='National')
    end_date = models.DateField(null=True, blank=True)
    current_update = models.DateField(auto_now=False, null=True, blank=True)
    next_update = models.DateField(auto_now=False, null=True, blank=True)
    next_status = models.CharField(max_length=50, default='unscheduled')
    datadelivery_status = models.CharField(max_length=50, default='')

    def save(self, *args, **kwargs):
        if not self.next_update:
            self.next_status = 'unscheduled'
        else:
            self.next_status = str(self.next_update) 

        if self.current_update and self.current_update > now_paris.date():
            self.datadelivery_status = 'awaiting'
        elif self.current_update and self.current_update == now_paris.date():
            self.datadelivery_status = 'received'
        else:
            self.datadelivery_status = 'delayed'
        super().save(*args, **kwargs)
    data_upload = models.FileField(null=True, blank=True)
    status = models.CharField(max_length=50, default='active') 
