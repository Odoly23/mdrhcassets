import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#creates your models here.
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class BaseModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="%(class)s_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="%(class)s_updated")
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="%(class)s_deleted")
    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = models.Manager()
    active_objects = ActiveManager()

    def soft_delete(self, user):
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save()

    def restore(self):
        self.deleted_at = None
        self.deleted_by = None
        self.save()

    class Meta:
        abstract = True

class Ministerio(BaseModel):
    code = models.CharField(max_length=10, null=True, blank=True, unique=True)
    name = models.CharField(max_length=200)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])


class Entity(BaseModel):
    name = models.CharField(max_length=150)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])


class Gabinete(BaseModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='gabinetes')
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])


class Unidade(BaseModel):
    gabinete = models.ForeignKey(Gabinete, on_delete=models.CASCADE, related_name='departments')
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])

class DG(BaseModel):
    entity = models.ForeignKey(Entity,on_delete=models.CASCADE, related_name='dgs')
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])

class DN(BaseModel):
    dg = models.ForeignKey(DG, on_delete=models.CASCADE, related_name='sub_dgs')
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])

class Departamento(BaseModel):
    dn = models.ForeignKey(DN, on_delete=models.CASCADE, related_name='departments')
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])

class Position(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])


class Category(BaseModel):
    name = models.CharField(max_length=100)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])

class SubCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])


class Brand(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])

class Model(BaseModel):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])


class Company(BaseModel):
    name = models.CharField(max_length=200)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])

class Year(models.Model):
    year = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])

class StatusInv(models.Model):
    name = models.CharField(max_length=100, verbose_name="Naran")
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])


class Status(models.Model):
    name = models.CharField(max_length=100, verbose_name="Naran")
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])

class Location(BaseModel):
    building = models.CharField(max_length=200)
    room = models.CharField(max_length=100)
    hashed = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hashed:
            self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
            super().save(update_fields=['hashed'])
