"""
Testes para TokenEnvioCargaViewSet e ViewSets Auxiliares
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
import uuid

from ..models import (
    TblPatriarca, TblTokenEnvioCarga, TblStatusProgresso,
    TblStatusTokenEnvioCarga, TblStatusCarga, TblTipoCarga,
)

User = get_user_model()


class TokenEnvioCargaViewSetTest(TestCase):
    """Testes para ViewSet de Token"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser_token@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.status_progresso = TblStatusProgresso.objects.get_or_create(
            id_status_progresso=1,
            defaults={'str_descricao': 'Em Progresso'}
        )[0]
        
        self.status_token = TblStatusTokenEnvioCarga.objects.get_or_create(
            id_status_token_envio_carga=1,
            defaults={'str_descricao': 'Ativo'}
        )[0]
        
        self.patriarca = TblPatriarca.objects.create(
            id_externo_patriarca=uuid.uuid4(),
            str_sigla_patriarca='SEGER',
            str_nome='Secretaria',
            id_status_progresso=self.status_progresso,
            dat_criacao=timezone.now(),
            id_usuario_criacao=self.user
        )
        
        self.token = TblTokenEnvioCarga.objects.create(
            id_patriarca=self.patriarca,
            id_status_token_envio_carga=self.status_token,
            str_token_retorno='TOKEN123',
            dat_data_hora_inicio=timezone.now()
        )
    
    def test_list_tokens(self):
        """Testa listagem de tokens"""
        response = self.client.get('/api/v1/carga/token/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_token(self):
        """Testa recuperação de token"""
        response = self.client.get(f'/api/v1/carga/token/{self.token.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['str_token_retorno'], 'TOKEN123')
    
    def test_validar_action(self):
        """Testa action validar"""
        response = self.client.get(f'/api/v1/carga/token/{self.token.pk}/validar/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('valido', response.data)
        self.assertTrue(response.data['valido'])
    
    def test_finalizar_action(self):
        """Testa action finalizar"""
        response = self.client.post(f'/api/v1/carga/token/{self.token.pk}/finalizar/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token.refresh_from_db()
        self.assertIsNotNone(self.token.dat_data_hora_fim)
    
    def test_estatisticas_action(self):
        """Testa action estatisticas"""
        response = self.client.get('/api/v1/carga/token/estatisticas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)


class AuxiliaryViewSetsTest(TestCase):
    """Testes para ViewSets auxiliares"""
    
    databases = {'default', 'gpp_plataform_db'}
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser_aux@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        TblStatusProgresso.objects.get_or_create(
            id_status_progresso=1,
            defaults={'str_descricao': 'Em Progresso'}
        )
        TblStatusCarga.objects.get_or_create(
            id_status_carga=1,
            defaults={'str_descricao': 'Iniciado', 'flg_sucesso': 0}
        )
        TblTipoCarga.objects.get_or_create(
            id_tipo_carga=1,
            defaults={'str_descricao': 'Organograma'}
        )
        TblStatusTokenEnvioCarga.objects.get_or_create(
            id_status_token_envio_carga=1,
            defaults={'str_descricao': 'Ativo'}
        )
    
    def test_list_status_progresso(self):
        """Testa listagem Status Progresso"""
        response = self.client.get('/api/v1/carga/status-progresso/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_status_carga(self):
        """Testa listagem Status Carga"""
        response = self.client.get('/api/v1/carga/status-carga/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_tipo_carga(self):
        """Testa listagem Tipo Carga"""
        response = self.client.get('/api/v1/carga/tipo-carga/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_status_token(self):
        """Testa listagem Status Token"""
        response = self.client.get('/api/v1/carga/status-token/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
