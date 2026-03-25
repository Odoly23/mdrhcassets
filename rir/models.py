import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from custom.models import BaseModel, Company, Category, SubCategory, Brand, Model


class Rir(BaseModel):
    ENTRY_TYPE_CHOICES = [
        ("PURCHASE", "Purchase"),
        ("DONATION", "Donation"),
    ]
    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]
    rir_no = models.CharField(max_length=20, unique=True, editable=False)
    container_no = models.CharField(max_length=50, blank=True, null=True)
    invoice_no = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPE_CHOICES)
    donor_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="rir_created")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="rir_approved")
    approved_at = models.DateTimeField(null=True, blank=True)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"RIR-{self.rir_no}"

    def save(self, *args, **kwargs):
        if not self.rir_no:
            self.rir_no = f"RIR-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)

        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=["hashed"])


class RirItem(BaseModel):
    rir = models.ForeignKey(Rir, on_delete=models.CASCADE, related_name="items")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])