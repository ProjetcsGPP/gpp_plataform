from django.db import models
from django.contrib.auth.models import BaseUserManager, Group, Permission
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
        managed = True

    def __str__(self):
        return f'{self.codigointerno} - {self.nomeaplicacao}'


class TblStatusUsuario(models.Model):
    """Status do usuário (Ativo, Inativo, etc.)"""
    idstatususuario = models.SmallIntegerField(primary_key=True, db_column='idstatususuario')
    strdescricao = models.CharField(max_length=100, db_column='strdescricao')

    class Meta:
        db_table = 'tblstatususuario'
        managed = True
        verbose_name = 'Status de Usuário'
        verbose_name_plural = 'Status de Usuários'

    def __str__(self):
        return self.strdescricao


class TblTipoUsuario(models.Model):
    """Tipo de usuário (Gestor, Técnico, etc.)"""
    idtipousuario = models.SmallIntegerField(primary_key=True, db_column='idtipousuario')
    strdescricao = models.CharField(max_length=100, db_column='strdescricao')

    class Meta:
        db_table = 'tbltipousuario'
        managed = True
        verbose_name = 'Tipo de Usuário'
        verbose_name_plural = 'Tipos de Usuários'

    def __str__(self):
        return self.strdescricao


class TblClassificacaoUsuario(models.Model):
    """Classificação do usuário"""
    idclassificacaousuario = models.SmallIntegerField(primary_key=True, db_column='idclassificacaousuario')
    strdescricao = models.CharField(max_length=100, db_column='strdescricao')

    class Meta:
        db_table = 'tblclassificacaousuario'
        managed = True
        verbose_name = 'Classificação de Usuário'
        verbose_name_plural = 'Classificações de Usuários'

    def __str__(self):
        return self.strdescricao


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if not password:
            raise ValueError("Superuser precisa de senha")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    id = models.BigAutoField(
        primary_key=True,
        db_column="idusuario"
    )

    name = models.CharField(
        max_length=200,
        db_column="strnome"
    )

    email = models.EmailField(
        max_length=200,
        unique=True,
        db_column="stremail"
    )

    password = models.CharField(
        max_length=200,
        db_column="strsenha"
    )

    # =====================
    # CAMPOS DJANGO AUTH
    # =====================

    is_active = models.BooleanField(
        default=True,
        db_column="is_active"
    )

    is_staff = models.BooleanField(
        default=False,
        db_column="is_staff"
    )

    is_superuser = models.BooleanField(
        default=False,
        db_column="is_superuser"
    )

    last_login = models.DateTimeField(
        null=True,
        blank=True,
        db_column="last_login"
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        db_column="date_joined"
    )

    # =====================
    # FK LEGADO (CORRIGIDO)
    # =====================

    idstatususuario = models.ForeignKey(
        TblStatusUsuario,
        on_delete=models.PROTECT,
        db_column="idstatususuario",
        default=1
    )

    idtipousuario = models.ForeignKey(
        TblTipoUsuario,
        on_delete=models.PROTECT,
        db_column="idtipousuario",
        default=1
    )

    idclassificacaousuario = models.ForeignKey(
        TblClassificacaoUsuario,
        on_delete=models.PROTECT,
        db_column="idclassificacaousuario",
        default=1
    )

    # =====================
    # AUDITORIA (dump)
    # =====================

    idusuariocriacao = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="idusuariocriacao",
        related_name="usuarios_criados"
    )

    idusuarioalteracao = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="idusuarioalteracao",
        related_name="usuarios_alterados"
    )

    datacriacao = models.DateTimeField(
        auto_now_add=True,
        db_column="datacriacao"
    )

    data_alteracao = models.DateTimeField(
        null=True,
        blank=True,
        db_column="data_alteracao"
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "tblusuario"
        managed = True

    def __str__(self):
        return self.email
class Role(models.Model):
    """RBAC por aplicação"""
    aplicacao = models.ForeignKey(Aplicacao, on_delete=models.CASCADE,
        null=True, db_column='aplicacao_id')
    nomeperfil = models.CharField(max_length=100)
    codigoperfil = models.CharField(max_length=100)

    class Meta:
        db_table = 'accounts_role'
        constraints = [
            models.UniqueConstraint(
                fields=["aplicacao", "codigoperfil"],  # ✅ Único por app + código
                name="uq_role_aplicacao_codigoperfil"
            )
        ]

    def __str__(self):
        return f'{self.aplicacao} / {self.codigoperfil}'


class UserRole(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    aplicacao = models.ForeignKey(Aplicacao, on_delete=models.CASCADE, null=True, db_column='aplicacao_id')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = 'accounts_userrole'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "aplicacao", "role"],  # ✅ CORRETO
                name="uq_userrole_user_aplicacao_role"
            )
        ]

    def __str__(self):
        return f'{self.user} → {self.aplicacao} ({self.role})'


class Attribute(models.Model):
    """ABAC por usuário/aplicação"""
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    aplicacao = models.ForeignKey(Aplicacao, on_delete=models.SET_NULL,
        null=True, db_column='aplicacao_id')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    class Meta:
        db_table = 'accounts_attribute'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "aplicacao", "key"],
                name="uq_userrole_aplicacao_key"
            )
        ]

    def __str__(self):
        return f'{self.user} / {self.aplicacao.codigointerno} / {self.key}={self.value}'