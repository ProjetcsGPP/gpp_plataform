# accounts/models.pyi
"""
Type stubs completos para models do accounts - Resolve todos os Pylance warnings
"""

from typing import Optional
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modelo customizado de usuário."""
    id: int
    email: str
    name: str  # Campo customizado
    cpf: str   # Campo customizado
    is_active: bool
    is_staff: bool
    is_superuser: bool


class Aplicacao(models.Model):
    """Modelo de aplicações da plataforma."""
    idaplicacao: int
    codigointerno: str
    nomeaplicacao: str
    base_url: Optional[str]
    isshowinportal: bool


class Role(models.Model):
    """Modelo de roles/perfis."""
    id: int
    codigoperfil: str
    nome: str


class UserRole(models.Model):
    """Relacionamento usuário-aplicação-role."""
    id: int
    user_id: int
    role_id: int
    aplicacao_id: int
    user: User
    aplicacao: Optional[Aplicacao]  # ✅ Pode ser None
    role: Role
