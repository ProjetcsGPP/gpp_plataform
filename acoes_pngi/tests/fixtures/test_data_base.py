"""Dados base reutilizáveis para todos os testes PNGI"""
from datetime import date
from typing import NamedTuple
from django.utils import timezone

from ...models import Eixo, SituacaoAcao, VigenciaPNGI


class BaseTestData(NamedTuple):
    """Estrutura de dados base para testes"""
    eixo: 'Eixo'
    situacao: 'SituacaoAcao'
    vigencia: 'VigenciaPNGI'


def create_base_test_data():
    """
    Cria ou recupera dados base para testes PNGI.
    
    Retorna:
        BaseTestData: Tupla com eixo, situacao e vigencia
    
    Nota:
        - Usa get_or_create para garantir idempotência
        - Dados fixos compartilhados por todos os testes
        - Executa UMA VEZ por classe de teste
    """
    from acoes_pngi.models import Eixo, SituacaoAcao, VigenciaPNGI
    
    # Eixo fixo para testes
    eixo_base, created = Eixo.objects.get_or_create(
        stralias="E1",
        defaults={'strdescricaoeixo': 'Eixo 1 - Teste Base'}
    )
    if created:
        print(f"✅ Eixo criado: {eixo_base}")
    
    # Situação fixa para testes
    situacao_base, created = SituacaoAcao.objects.get_or_create(
        strdescricaosituacao="EM_ANDAMENTO",
        defaults={'strdescricaosituacao': 'EM_ANDAMENTO'}
    )
    if created:
        print(f"✅ Situação criada: {situacao_base}")
    
    # Vigência fixa para testes
    vigencia_base, created = VigenciaPNGI.objects.get_or_create(
        strdescricaovigenciapngi="PNGI 2026 - Testes",
        defaults={
            'datiniciovigencia': date(2026, 1, 1),
            'datfinalvigencia': date(2026, 12, 31),
            'isvigenciaativa': True
        }
    )
    if created:
        print(f"✅ Vigência criada: {vigencia_base}")
    
    return BaseTestData(eixo=eixo_base, situacao=situacao_base, vigencia=vigencia_base)
