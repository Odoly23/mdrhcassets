import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from custom.models import Model, Brand, Category, SubCategory, BaseModel, Company, \
						  Ministerio, Year, Status, Location
from rir.models import RirItem

# Create your models here.
class Asset(BaseModel):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("DAMAGED", "Damaged"),
        ("DISPOSED", "Disposed"),
    ]
    rir_item = models.ForeignKey(RirItem, on_delete=models.CASCADE, related_name="assets")
    asset_code = models.CharField(max_length=30, unique=True, editable=False)
    barcode = models.CharField(max_length=50, unique=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    is_distributed = models.BooleanField(default=False)
    distributed_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    current_condition = models.CharField(max_length=20, choices=[('good', 'Good'), ('damaged', 'Damaged'),('repair', 'Under Repair')],default='good')
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.asset_code} - {self.category}"

    def save(self, *args, **kwargs):
        if not self.asset_code:
            self.asset_code = f"AST-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=["hashed"])