"""
Testes dos serializers de Acoes PNGI.
"""

from django.test import TestCase
from .base import BaseTestCase, BaseAPITestCase
from acoes_pngi.models import Eixo, SituacaoAcao, VigenciaPNGI
from acoes_pngi.serializers import (
    EixoSerializer,
    SituacaoAcaoSerializer,
    VigenciaPNGISerializer
)
from datetime import date
from django.utils import timezone


class EixoSerializerTest(BaseTestCase):
    """Testes do EixoSerializer"""
    
    # Precisa de ambos databases: default para User e gpp_plataform_db para Eixo
    databases = {'default', 'gpp_plataform_db'}
    
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
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        eixo = serializer.save()
        self.assertEqual(eixo.strdescricaoeixo, 'Transformação Digital')


class VigenciaPNGISerializerTest(BaseTestCase):
    """Testes do VigenciaPNGISerializer"""
    
    # Precisa de ambos databases
    databases = {'default', 'gpp_plataform_db'}
    
    def test_serialize_vigencia(self):
        """Testa serialização de vigência"""
        vigencia = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2024-2028',
            datiniciovigencia=date(2024, 1, 1,
            datfinalvigencia=date(2024, 12, 31)),
            datfinalvigencia=date(2028, 12, 31),
            isvigenciaativa=True
        )
        
        serializer = VigenciaPNGISerializer(vigencia)
        data = serializer.data
        
        self.assertEqual(data['strdescricaovigenciapngi'], 'PNGI 2024-2028')
        self.assertTrue(data['isvigenciaativa'])
        self.assertIn('idvigenciapngi', data)
