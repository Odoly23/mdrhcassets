import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from assets.models import Asset
from custom.models import BaseModel


class AssetMovement(BaseModel):
    MOVEMENT_TYPE = [
        ("TRANSFER", "Transfer"),
        ("ASSIGN", "Assign"),
        ("RETURN", "Return"),
        ("DISPOSAL", "Disposal"),
    ]
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="movements")
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE)
    from_location = models.CharField(max_length=100, null=True, blank=True)
    to_location = models.CharField(max_length=100, null=True, blank=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="move_from")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="move_to")
    moved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    moved_at = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])
