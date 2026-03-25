from django.db import models
from custom.models import Model, Brand, Category, SubCategory, BaseModel, Company, \
						  Ministerio, Year, Status, Location, Gabinete, DG, DN, \
						  Unidade, Entity, Departamento, StatusInv
from rir.models import RirItem
from staff.models import Employee
from django.contrib.auth.models import User
from assets.models import Asset
from django.utils import timezone
import hashlib

# Create your models here.
class Distribution(BaseModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='distributions')
    ministerio = models.ForeignKey(Ministerio, on_delete=models.CASCADE, null=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True)
    gabinete = models.ForeignKey(Gabinete, on_delete=models.CASCADE, null=True, blank=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, null=True, blank=True)
    dg = models.ForeignKey(DG, on_delete=models.CASCADE, null=True, blank=True,  verbose_name="Diresaun Geral")
    dn = models.ForeignKey(DN, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True,  verbose_name="Departamento")
    emp = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    condition =models.ForeignKey(StatusInv, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)
    date_assigned = models.DateField()
    is_return = models.BooleanField(default=False)
    date_returned = models.DateField(null=True, blank=True)
    is_conf = models.BooleanField(default=False)
    date_conf = models.DateField(null=True, blank=True)
    conf_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="distconf")
    is_appr = models.BooleanField(default=False)
    date_appr = models.DateField(null=True, blank=True)
    appr_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='distappr')
    note = models.TextField(blank=True)
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