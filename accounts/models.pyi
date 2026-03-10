# accounts/models.pyi
"""
Type stubs para models do accounts.
Reflexo fiel do accounts/models.py - atualizado para refatoração UserProfile v2.

Regras:
- User é o padrão do Django (auth.User) - NÃO é customizado.
- Campos extras (cpf, name) vivem em UserProfile.
- Todos os modelos declarados aqui devem existir no models.py real.
"""

from typing import Optional
from django.contrib.auth.models import User
from django.db import models


# =====================
# TABELAS AUXILIARES
# =====================

class StatusUsuario(models.Model):
    idstatususuario: int
    strdescricao: str


class TipoUsuario(models.Model):
    idtipousuario: int
    strdescricao: str


class ClassificacaoUsuario(models.Model):
    idclassificacaousuario: int
    strdescricao: str


class Aplicacao(models.Model):
    idaplicacao: int
    codigointerno: str
    nomeaplicacao: str
    base_url: Optional[str]
    isshowinportal: bool


# =====================
# USER PROFILE (EXTENSÃO DO auth.User)
# =====================

class UserProfile(models.Model):
    """
    Extensão do User padrão do Django.
    Relacionamento OneToOne com auth.User via user_id (PK).
    Campos extras de negócio e auditoria ficam aqui.
    """
    user: User                              # OneToOneField -> auth.User (PK)
    name: str                               # strnome
    cpf: str                                # campo de CPF (se existir)
    status_usuario: StatusUsuario
    tipo_usuario: TipoUsuario
    classificacao_usuario: ClassificacaoUsuario
    idusuariocriacao: Optional[User]
    idusuarioalteracao: Optional[User]
    datacriacao: str                        # DateTimeField
    data_alteracao: Optional[str]           # DateTimeField nullable


# =====================
# RBAC - ROLES E PERMISSÕES
# =====================

class Role(models.Model):
    id: int
    aplicacao: Optional[Aplicacao]
    nomeperfil: str
    codigoperfil: str


class UserRole(models.Model):
    id: int
    user: User
    aplicacao: Optional[Aplicacao]
    role: Role


class Attribute(models.Model):
    id: int
    user: User
    aplicacao: Optional[Aplicacao]
    key: str
    value: str
