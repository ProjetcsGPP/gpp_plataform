"""
Testes dos serializers de Acoes PNGI.
"""

from django.test import TestCase
from acoes_pngi.models import Eixo, SituacaoAcao, VigenciaPNGI
from acoes_pngi.serializers import (
    EixoSerializer,
    SituacaoAcaoSerializer,
    VigenciaPNGISerializer
)
from datetime import date


class EixoSerializerTest(TestCase):
    """Testes do EixoSerializer"""
    
    def test_serialize_eixo(self):
        """Testa serialização de eixo"""
        eixo = Eixo.objects.create(
            strdescricaoeixo='Governança Digital',
            stralias='GD'
        )
        
        serializer = EixoSerializer(eixo)
        data = serializer.data
        
        self.assertEqual(data['strdescricaoeixo'], 'Governança Digital')
        self.assertEqual(data['stralias'], 'GD')
        self.assertIn('ideixo', data)
    
    def test_create_eixo(self):
        """Testa criação via serializer"""
        data = {
            'strdescricaoeixo': 'Transformação Digital',
            'stralias': 'TD'
        }
        
        serializer = EixoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        eixo = serializer.save()
        self.assertEqual(eixo.strdescricaoeixo, 'Transformação Digital')


class VigenciaPNGISerializerTest(TestCase):
    """Testes do VigenciaPNGISerializer"""
    
    def test_serialize_vigencia(self):
        """Testa serialização de vigência"""
        vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2024-2028',
            datiniciovigencia=date(2024, 1, 1),
            datfinalvigencia=date(2028, 12, 31),
            isvigenciaativa=True
        )
        
        serializer = VigenciaPNGISerializer(vigencia)
        data = serializer.data
        
        self.assertEqual(data['strdescricaovigenciapngi'], 'PNGI 2024-2028')
        self.assertTrue(data['isvigenciaativa'])
        self.assertIn('esta_vigente', data)
        self.assertIn('duracao_dias', data)

