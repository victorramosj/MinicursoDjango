from django.db import models


# Modelo: Colaboradores (Agora utilizando o modelo padrão do Django)
class Colaborador(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)  # Relacionamento com o User
    telefone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    cargo = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='colaboradores/photos/', null=True, blank=True)
    
    def __str__(self):
        return self.user.username


# Modelo: Clientes (Também utilizando o modelo padrão do Django)
class Cliente(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)  # Relacionamento com o User
    telefone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    dt_nasc = models.DateField(null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True)
    photo = models.ImageField(upload_to='clientes/photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username
