#!/usr/bin/env python
"""
Cria Alexandre com perfis GESTOR - Robusto e idempotente
"""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gpp_plataform.settings")
django.setup()

from django.contrib.auth import get_user_model

from accounts.models import Aplicacao, Role, UserRole

User = get_user_model()

# 1. Superusuário Alexandre
alexandre, created = User.objects.get_or_create(
    email="alexandre.mohamad@seger.es.gov.br",
    defaults={
        "name": "Alexandre Wanick Mohamad",
        "is_staff": True,
        "is_active": True,
    },
)

if created:
    alexandre.set_password("seger2026")
    alexandre.save()
    print("✅ Usuário Alexandre CRIADO")
else:
    print("ℹ️ Usuário Alexandre atualizado")

# 2. Perfis GESTOR específicos
perfis_desejados = {
    "GESTOR_PORTAL": "PORTAL",
    "GESTOR_PNGI": "ACOES_PNGI",
    "GESTOR_CARGA": "CARGA_ORG_LOT",
}

atribuidos = []
for codigoperfil, codigointerno_app in perfis_desejados.items():
    try:
        aplicacao = Aplicacao.objects.get(codigointerno=codigointerno_app)
        role = Role.objects.get(codigoperfil=codigoperfil, aplicacao=aplicacao)

        userrole, created = UserRole.objects.get_or_create(
            user=alexandre, aplicacao=aplicacao, role=role
        )

        if created:
            print(f"✅ {codigoperfil} ATRIBUÍDO")
        else:
            print(f"ℹ️  {codigoperfil} já existia")

        atribuidos.append(codigoperfil)

    except Aplicacao.DoesNotExist:
        print(f"❌ Aplicação {codigointerno_app} não encontrada")
    except Role.DoesNotExist:
        print(f"❌ Role {codigoperfil} não encontrada")

print("\n🎉 RESUMO:")
print(f"Usuário: {alexandre.email}")
print(f"Perfis: {', '.join(atribuidos)}")
print(f"Admin Django: {'✅' if alexandre.is_staff else '❌'}")
print("\nLogin: http://127.0.0.1:8000/admin/")
print("Senha: seger2026 (ALTERE EM PROD!)")
