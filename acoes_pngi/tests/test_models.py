"""
Testes dos modelos de Acoes PNGI.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
from acoes_pngi.models import Eixo, SituacaoAcao, VigenciaPNGI


class EixoModelTest(TestCase):
    """Testes do modelo Eixo"""
    
    def test_create_eixo(self):
        """Testa criação de eixo"""
        eixo = Eixo.objects.create(
            strdescricaoeixo='Governança Digital',
            stralias='GD'
        )
        
        self.assertEqual(eixo.strdescricaoeixo, 'Governança Digital')
        self.assertEqual(eixo.stralias, 'GD')
    
    def test_alias_uppercase(self):
        """Testa que alias é convertido para maiúsculas"""
        eixo = Eixo.objects.create(
            strdescricaoeixo='Test',
            stralias='test'
        )
        eixo.clean()
        
        self.assertEqual(eixo.stralias, 'TEST')
    
    def test_unique_alias(self):
        """Testa unicidade do alias"""
        Eixo.objects.create(
            strdescricaoeixo='First',
            stralias='E1'
        )
        
        with self.assertRaises(Exception):
            Eixo.objects.create(
                strdescricaoeixo='Second',
                stralias='E1'
            )
    
    def test_str_representation(self):
        """Testa string representation"""
        eixo = Eixo.objects.create(
            strdescricaoeixo='Governança Digital',
            stralias='GD'
        )
        
        self.assertEqual(str(eixo), 'GD - Governança Digital')


class SituacaoAcaoModelTest(TestCase):
    """Testes do modelo SituacaoAcao"""
    
    def test_create_situacao(self):
        """Testa criação de situação"""
        situacao = SituacaoAcao.objects.create(
            strdescricaosituacao='Em andamento'
        )
        
        self.assertEqual(situacao.strdescricaosituacao, 'Em andamento')
    
    def test_unique_descricao(self):
        """Testa unicidade da descrição"""
        SituacaoAcao.objects.create(strdescricaosituacao='Concluída')
        
        with self.assertRaises(Exception):
            SituacaoAcao.objects.create(strdescricaosituacao='Concluída')


class VigenciaPNGIModelTest(TestCase):
    """Testes do modelo VigenciaPNGI"""
    
    def test_create_vigencia(self):
        """Testa criação de vigência"""
        vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2024-2028',
            datiniciovigencia=date(2024, 1, 1),
            datfinalvigencia=date(2028, 12, 31),
            isvigenciaativa=True
        )
        
        self.assertEqual(vigencia.strdescricaovigenciapngi, 'PNGI 2024-2028')
        self.assertTrue(vigencia.isvigenciaativa)
    
    def test_validation_data_final_maior(self):
        """Testa validação: data final deve ser maior que inicial"""
        vigencia = VigenciaPNGI(
            strdescricaovigenciapngi='Invalid',
            datiniciovigencia=date(2024, 12, 31),
            datfinalvigencia=date(2024, 1, 1),
            isvigenciaativa=True
        )
        
        with self.assertRaises(ValidationError):
            vigencia.save()
    
    def test_esta_vigente_property(self):
        """Testa propriedade esta_vigente"""
        hoje = timezone.now().date()
        
        vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='Current',
            datiniciovigencia=hoje - timedelta(days=10),
            datfinalvigencia=hoje + timedelta(days=10),
            isvigenciaativa=True
        )
        
        self.assertTrue(vigencia.esta_vigente)
    
    def test_nao_esta_vigente_inativa(self):
        """Testa que vigência inativa não está vigente"""
        hoje = timezone.now().date()
        
        vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='Inactive',
            datiniciovigencia=hoje - timedelta(days=10),
            datfinalvigencia=hoje + timedelta(days=10),
            isvigenciaativa=False
        )
        
        self.assertFalse(vigencia.esta_vigente)
    
    def test_duracao_dias_property(self):
        """Testa cálculo de duração em dias"""
        vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='Test',
            datiniciovigencia=date(2024, 1, 1),
            datfinalvigencia=date(2024, 12, 31),
            isvigenciaativa=True
        )
        
        # 365 dias (2024 é ano bissexto)
        self.assertEqual(vigencia.duracao_dias, 365)
