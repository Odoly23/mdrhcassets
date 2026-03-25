import hashlib, datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from custom.models import (BaseModel, Ministerio, Entity, Gabinete, Unidade, DG, DN, Departamento, Position)
from config.utils_upload import upload_photo

class StaffStatus(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Naran")
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])


class Employee(BaseModel):
    id_funs = models.CharField(max_length=20, null=True, blank=True, verbose_name="Id Funsionario")
    first_name = models.CharField(max_length=30, null=True, verbose_name="Naran")
    last_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="Apelidu")
    place_of_birth = models.CharField(max_length=100, blank=True, null=True, verbose_name="Fatin Moris")
    date_of_birth = models.DateField(null=True, verbose_name="Data Moris")
    sex = models.CharField(choices=[('Mane','Mane'),('Feto','Feto')], max_length=6, null=True, blank=True, verbose_name="Sexu")
    status = models.ForeignKey(StaffStatus, on_delete=models.CASCADE, null=True, verbose_name="Status")
    datetime = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default='default.png', upload_to=upload_photo, null=True)
    hashed = models.CharField(max_length=32, null=True)
    
    def __str__(self):
        template = '{0.first_name} {0.last_name}'
        return template.format(self)

    def age(self):
        return int((datetime.date.today() - self.date_of_birth).days / 365)

class EmployeeUser(BaseModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="employeeuser")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        template = '{0.employee} {0.user}'
        return template.format(self)


class EmployeePosition(BaseModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="employeeposition", verbose_name="Pessoal")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name="employeeposition", verbose_name="Pojisaun")
    
    def __str__(self):
        template = '{0.position}'
        return template.format(self)

class EmployeeDivision(BaseModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="employeedivision", verbose_name="Pessoal")
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True)
    gabinete = models.ForeignKey(Gabinete, on_delete=models.CASCADE, null=True, blank=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, null=True, blank=True)
    dg = models.ForeignKey(DG, on_delete=models.CASCADE, null=True, blank=True, related_name="employedg", verbose_name="Diresaun Geral")
    dn = models.ForeignKey(DN, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True,  verbose_name="Departamento")
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        template = '{0.employee}'
        return template.format(self)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])
