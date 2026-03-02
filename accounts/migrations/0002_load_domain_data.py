# accounts/migrations/0002_load_domain_data.py
from django.db import migrations

def load_domain_data(apps, schema_editor):
    """
    Migração CONSOLIDADA ACCOUNTS - APENAS DADOS DE DOMÍNIO (SEM GROUPS DJANGO)
    ✅ Status/Tipo/Classificação Usuario
    ✅ 3 Aplicações GPP Platform  
    ✅ 10 Roles/Perfis (todas aplicações)
    ❌ Groups Django + Permissões PNGI (movido para acoes_pngi/0003)
    """
    
    # 1. STATUS USUÁRIO
    TblStatusUsuario = apps.get_model('accounts', 'TblStatusUsuario')
    status_data = [
        {'idstatususuario': 1, 'strdescricao': 'Ativo'},
        {'idstatususuario': 2, 'strdescricao': 'Inativo'},
    ]
    for item in status_data:
        TblStatusUsuario.objects.get_or_create(**item)
    print("✅ Status Usuario carregados")
    
    # 2. TIPO USUÁRIO
    TblTipoUsuario = apps.get_model('accounts', 'TblTipoUsuario')
    tipo_data = [
        {'idtipousuario': 1, 'strdescricao': 'Interno'},
        {'idtipousuario': 2, 'strdescricao': 'Externo'},
    ]
    for item in tipo_data:
        TblTipoUsuario.objects.get_or_create(**item)
    print("✅ Tipo Usuario carregados")
    
    # 3. CLASSIFICAÇÃO USUÁRIO
    TblClassificacaoUsuario = apps.get_model('accounts', 'TblClassificacaoUsuario')
    classificacao_data = [
        {'idclassificacaousuario': 1, 'strdescricao': 'Padrão'},
    ]
    for item in classificacao_data:
        TblClassificacaoUsuario.objects.get_or_create(**item)
    print("✅ Classificação Usuario carregada")
    
    # 4. APLICAÇÕES
    Aplicacao = apps.get_model('accounts', 'Aplicacao')
    aplicacoes_data = [
        {
            'idaplicacao': 1,
            'codigointerno': 'PORTAL',
            'nomeaplicacao': 'Portal GPP',
            'base_url': 'http://127.0.0.1:8000/portal/',
            'isshowinportal': False
        },
        {
            'idaplicacao': 2,
            'codigointerno': 'CARGA_ORG_LOT',
            'nomeaplicacao': 'Carga Única de Organograma e Lotação',
            'base_url': 'http://127.0.0.1:8000/carga_org_lot/',
            'isshowinportal': True
        },
        {
            'idaplicacao': 3,
            'codigointerno': 'ACOES_PNGI',
            'nomeaplicacao': 'Ações PNGI',
            'base_url': 'http://127.0.0.1:8000/acoes-pngi/',
            'isshowinportal': True
        }
    ]
    for data in aplicacoes_data:
        if not Aplicacao.objects.filter(codigointerno=data['codigointerno']).exists():
            aplicacao = Aplicacao(**data)
            aplicacao.save(using=schema_editor.connection.alias)
            print(f"✅ Aplicação criada: {data['codigointerno']}")
    
    # 5. ROLES/PERFIS
    Role = apps.get_model('accounts', 'Role')
    roles_data = [
        # PORTAL
        {'id': 1, 'nomeperfil': 'Usuario do Portal', 'codigoperfil': 'USER_PORTAL', 'aplicacao_id': 1},
        {'id': 4, 'nomeperfil': 'Gestor do Portal', 'codigoperfil': 'GESTOR_PORTAL', 'aplicacao_id': 1},
        # CARGA_ORG_LOT
        {'id': 2, 'nomeperfil': 'Gestor Carga Org/Lot', 'codigoperfil': 'GESTOR_CARGA', 'aplicacao_id': 2},
        {'id': 20, 'nomeperfil': 'Coordenador - Gerencia Configurações', 'codigoperfil': 'COORDENADOR_CARGA', 'aplicacao_id': 2},
        {'id': 21, 'nomeperfil': 'Analista - Upload e Validação', 'codigoperfil': 'ANALISTA_CARGA', 'aplicacao_id': 2},
        {'id': 22, 'nomeperfil': 'Consultor - Apenas Leitura', 'codigoperfil': 'VISUALIZADOR_CARGA', 'aplicacao_id': 2},
        # ACOES_PNGI
        {'id': 3, 'nomeperfil': 'Gestor Acoes PNGI', 'codigoperfil': 'GESTOR_PNGI', 'aplicacao_id': 3},
        {'id': 5, 'nomeperfil': 'Coordenador - Gerencia Configurações', 'codigoperfil': 'COORDENADOR_PNGI', 'aplicacao_id': 3},
        {'id': 6, 'nomeperfil': 'Operador - Apenas Ações', 'codigoperfil': 'OPERADOR_ACAO', 'aplicacao_id': 3},
        {'id': 7, 'nomeperfil': 'Consultor - Apenas Leitura', 'codigoperfil': 'CONSULTOR_PNGI', 'aplicacao_id': 3},
    ]
    for item in roles_data:
        Role.objects.get_or_create(id=item['id'], defaults=item)
    print("✅ Todas as Roles/Perfis carregadas")

def reverse_migration(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            load_domain_data,
            reverse_code=reverse_migration
        ),
    ]
