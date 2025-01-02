from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now

# Gerenciador de usuários personalizado
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Modelo: Colaboradores (Baseado no modelo de usuário do Django)
class Colaborador(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    senha = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    referencias = models.TextField(null=True, blank=True)
    cargo = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='colaboradores/photos/', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cpf']

    def __str__(self):
        return self.nome


# Modelo: Clientes
class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    referencias = models.TextField(null=True, blank=True)
    dt_nasc = models.DateField(null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True)
    photo = models.ImageField(upload_to='clientes/photos/', null=True, blank=True)

    def __str__(self):
        return self.nome