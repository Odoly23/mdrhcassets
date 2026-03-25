import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from custom.models import Model, Brand, Category, SubCategory, BaseModel, Company, \
						  Ministerio, Year, Status, Location
from rir.models import RirItem
from assets.models import Asset

class AssetMaintenance(BaseModel):
    STATUS_CHOICES = [
        ("SCHEDULED", "Scheduled"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="maintenances")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    scheduled_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    vendor = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="SCHEDULED")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])
