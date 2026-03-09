"""
Admin configuration para accounts app.
Combina auth.User com UserProfile usando InlineModelAdmin.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    UserProfile,
    Aplicacao,
    TblStatusUsuario,
    TblTipoUsuario,
    TblClassificacaoUsuario,
    Role,
    UserRole,
    Attribute,
)


# =====================
# USER PROFILE INLINE
# =====================

class UserProfileInline(admin.StackedInline):
    """
    Inline admin para UserProfile dentro do User admin.
    """
    model = UserProfile
    can_delete = False
    verbose_name = 'Profile'
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = (
        'name',
        'idstatususuario',
        'idtipousuario',
        'idclassificacaousuario',
        'datacriacao',
        'data_alteracao',
    )
    readonly_fields = ('datacriacao', 'data_alteracao')


class CustomUserAdmin(BaseUserAdmin):
    """
    Customização do UserAdmin para incluir UserProfile inline.
    """
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')


# Unregister o User padrão e registra o customizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# =====================
# TABELAS AUXILIARES
# =====================

@admin.register(Aplicacao)
class AplicacaoAdmin(admin.ModelAdmin):
    list_display = ('idaplicacao', 'codigointerno', 'nomeaplicacao', 'isshowinportal')
    list_filter = ('isshowinportal',)
    search_fields = ('codigointerno', 'nomeaplicacao')


@admin.register(TblStatusUsuario)
class StatusUsuarioAdmin(admin.ModelAdmin):
    list_display = ('idstatususuario', 'strdescricao')
    search_fields = ('strdescricao',)


@admin.register(TblTipoUsuario)
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('idtipousuario', 'strdescricao')
    search_fields = ('strdescricao',)


@admin.register(TblClassificacaoUsuario)
class ClassificacaoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('idclassificacaousuario', 'strdescricao')
    search_fields = ('strdescricao',)


# =====================
# RBAC - ROLES E PERMISSIONS
# =====================

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('aplicacao', 'codigoperfil', 'nomeperfil')
    list_filter = ('aplicacao',)
    search_fields = ('codigoperfil', 'nomeperfil')


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'aplicacao', 'role')
    list_filter = ('aplicacao', 'role')
    search_fields = ('user__username', 'user__email')
    autocomplete_fields = ['user']


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('user', 'aplicacao', 'key', 'value')
    list_filter = ('aplicacao', 'key')
    search_fields = ('user__username', 'user__email', 'key', 'value')
    autocomplete_fields = ['user']
