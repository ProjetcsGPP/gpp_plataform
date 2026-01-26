from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class Aplicacao(models.Model):
    idaplicacao = models.AutoField(primary_key=True)
    codigointerno = models.CharField(max_length=50, unique=True)
    nomeaplicacao = models.CharField(max_length=200)
    base_url = models.URLField(blank=True, null=True)
    isshowinportal = models.BooleanField(default=True)

    class Meta:
        db_table = 'tblaplicacao'
        managed = True  # se já existe no banco

    def __str__(self):
        return f'{self.codigointerno} - {self.nomeaplicacao}'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)  # grava hash em `password`
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if not password:
            raise ValueError("Superuser precisa de senha")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # Mapeia para colunas existentes do dump
    id = models.BigAutoField(primary_key=True, db_column="idusuario")
    name = models.CharField(max_length=200, db_column="strnome")
    email = models.EmailField(max_length=200, unique=True, db_column="stremail")

    # IMPORTANTÍSSIMO: Django usa o campo "password" internamente,
    # então mapeamos password -> strsenha
    password = models.CharField(max_length=200, db_column="strsenha")

    # Campos “Django” que você adicionou via ALTER TABLE
    is_active = models.BooleanField(default=True, db_column="is_active")
    is_staff = models.BooleanField(default=False, db_column="is_staff")
    is_superuser = models.BooleanField(default=False, db_column="is_superuser")
    last_login = models.DateTimeField(null=True, blank=True, db_column="last_login")
    date_joined = models.DateTimeField(null=True, blank=True, db_column="date_joined")

    # Campos existentes no dump que são NOT NULL (precisam existir no model com default)
    idstatususuario = models.SmallIntegerField(default=1, db_column="idstatususuario")
    idtipousuario = models.SmallIntegerField(default=1, db_column="idtipousuario")
    idclassificacaousuario = models.SmallIntegerField(default=1, db_column="idclassificacaousuario")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "tblusuario"
        managed = True  # se já existe no banco

    def __str__(self):
        return self.email


class Role(models.Model):
    """
    RBAC por aplicação (sem empresa).
    Ex: 'Gestor Portal', 'Gestor Carga', etc.
    """
    #aplicacao = models.ForeignKey(Aplicacao, on_delete=models.CASCADE)
    aplicacao = models.ForeignKey(Aplicacao,  on_delete=models.CASCADE,
        null=True,
        db_column='aplicacao_id')
    nomeperfil = models.CharField(max_length=100)
    codigoperfil = models.CharField(max_length=100)

    class Meta:
        db_table = 'accounts_role'
        unique_together = ('aplicacao', 'codigoperfil')

    def __str__(self):
        return f'{self.aplicacao} / {self.codigoperfil}'


class UserRole(models.Model):
    """
    User 1 → N Aplicacao via roles.
    Um usuário pode ter múltiplas aplicações.
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    #aplicacao = models.ForeignKey(Aplicacao, on_delete=models.CASCADE)
    aplicacao = models.ForeignKey(Aplicacao,  on_delete=models.CASCADE,
        null=True,
        db_column='aplicacao_id')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = 'accounts_userrole'
        unique_together = ('user', 'aplicacao', 'role')

    def __str__(self):
        return f'{self.user} → {self.aplicacao} ({self.role})'


class Attribute(models.Model):
    """
    ABAC por usuário/aplicação (sem empresa).
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    aplicacao = models.ForeignKey(Aplicacao,  on_delete=models.SET_NULL,
        null=True,
        db_column='aplicacao_id')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    class Meta:
        db_table = 'accounts_attribute'
        unique_together = ('user', 'aplicacao', 'key')

    def __str__(self):
        return f'{self.user} / {self.aplicacao.codigointerno} / {self.key}={self.value}'

