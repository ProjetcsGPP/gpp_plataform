from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Aplicacao, Role, UserRole, Attribute


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ("email",)
    list_display = ("email", "name", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "name")

    fieldsets = (
        (None, {"fields": ("email", "password", "name")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "name", "password1", "password2", "is_staff", "is_superuser")}),
    )

    # Diz ao admin que o "username" não existe
    def get_fieldsets(self, request, obj=None):
        return super().get_fieldsets(request, obj)    

@admin.register(Aplicacao)
class AplicacaoAdmin(admin.ModelAdmin):
    list_display = ('codigointerno', 'nomeaplicacao', 'base_url')
    search_fields = ('codigointerno', 'nomeaplicacao')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('aplicacao', 'codigoperfil', 'nomeperfil')
    list_filter = ('aplicacao',)
    search_fields = ('codigoperfil', 'nomeperfil')

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'aplicacao', 'role')
    list_filter = ('aplicacao', 'role')
    search_fields = ('user__username',)

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('user', 'aplicacao', 'key', 'value')
    list_filter = ('aplicacao', 'key')
    search_fields = ('user__username', 'key', 'value')
    
