import requests
import logging
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import transaction
from accounts.models import User
from db_service.models import AppClient

logger = logging.getLogger(__name__)


class PortalAuthService:
    """
    Serviço para integração com o Portal de Autenticação.
    Gerencia validação de tokens e sincronização de usuários.
    """
    
    def __init__(self):
        self.portal_url = getattr(settings, 'PORTAL_AUTH_URL', None)
        self.app_code = getattr(settings, 'APP_CODE', 'ACOES_PNGI')
        
        if not self.portal_url:
            logger.warning("PORTAL_AUTH_URL não configurado no settings")
    
    def validate_token(self, token):
        """
        Valida o token junto ao Portal de Autenticação.
        
        Args:
            token (str): Token JWT recebido do portal
            
        Returns:
            dict: Dados do usuário se válido, None caso contrário
        """
        if not self.portal_url:
            logger.error("Portal URL não configurado")
            return None
        
        try:
            url = f"{self.portal_url}/api/auth/validate-token/"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                url,
                headers=headers,
                json={'app_code': self.app_code},
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                logger.info(f"Token validado com sucesso para usuário: {user_data.get('email')}")
                return user_data
            else:
                logger.warning(f"Falha na validação do token: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao validar token no portal: {str(e)}")
            return None
    
    def get_or_create_user_from_portal(self, user_data):
        """
        Busca ou cria um usuário localmente baseado nos dados do portal.
        
        Args:
            user_data (dict): Dados do usuário retornados pelo portal
            
        Returns:
            User: Instância do usuário
        """
        try:
            email = user_data.get('email')
            name = user_data.get('name', email)
            
            if not email:
                logger.error("Email não encontrado nos dados do usuário")
                return None
            
            # Busca ou cria o usuário
            with transaction.atomic():
                user, created = User.objects.get_or_create(
                    stremail=email,
                    defaults={
                        'strnome': name,
                        'strsenha': make_password(None),  # Senha aleatória (não será usada)
                        'idtipousuario': 1,
                        'idstatususuario': 1,
                        'idclassificacaousuario': 2,  # Gestor Aplicação
                        'is_active': True,
                        'is_staff': False,
                        'is_superuser': False,
                    }
                )
                
                if created:
                    logger.info(f"Novo usuário criado localmente: {email}")
                else:
                    # Atualiza nome se mudou
                    if user.strnome != name:
                        user.strnome = name
                        user.save()
                        logger.info(f"Nome do usuário atualizado: {email}")
                
                return user
                
        except Exception as e:
            logger.error(f"Erro ao criar/buscar usuário: {str(e)}")
            return None
    
    def authenticate_user(self, token):
        """
        Autentica usuário via token do portal.
        Valida o token e sincroniza o usuário localmente.
        
        Args:
            token (str): Token JWT do portal
            
        Returns:
            User: Instância do usuário autenticado ou None
        """
        user_data = self.validate_token(token)
        
        if not user_data:
            return None
        
        user = self.get_or_create_user_from_portal(user_data)
        return user
    
    def get_user_roles(self, email):
        """
        Busca os perfis/roles do usuário no portal.
        
        Args:
            email (str): Email do usuário
            
        Returns:
            list: Lista de roles do usuário para esta aplicação
        """
        try:
            user = User.objects.get(stremail=email)
            
            # Busca roles através do modelo accounts
            from accounts.models import UserRole
            roles = UserRole.objects.filter(
                user=user,
                aplicacao__codigointerno=self.app_code
            ).select_related('role', 'aplicacao')
            
            return [
                {
                    'role_id': ur.role.id,
                    'role_code': ur.role.codigoperfil,
                    'role_name': ur.role.nomeperfil,
                    'app_code': ur.aplicacao.codigointerno,
                }
                for ur in roles
            ]
            
        except User.DoesNotExist:
            logger.warning(f"Usuário não encontrado: {email}")
            return []
        except Exception as e:
            logger.error(f"Erro ao buscar roles do usuário: {str(e)}")
            return []
    
    def get_user_attributes(self, email):
        """
        Busca os atributos customizados do usuário.
        
        Args:
            email (str): Email do usuário
            
        Returns:
            dict: Dicionário de atributos (key: value)
        """
        try:
            user = User.objects.get(stremail=email)
            
            # Busca atributos através do modelo accounts
            from accounts.models import Attribute
            attributes = Attribute.objects.filter(
                user=user,
                aplicacao__codigointerno=self.app_code
            )
            
            return {
                attr.key: attr.value
                for attr in attributes
            }
            
        except User.DoesNotExist:
            logger.warning(f"Usuário não encontrado: {email}")
            return {}
        except Exception as e:
            logger.error(f"Erro ao buscar atributos do usuário: {str(e)}")
            return {}
    
    def create_app_client(self, client_id, client_secret):
        """
        Cria credenciais de client para esta aplicação.
        
        Args:
            client_id (str): ID do client
            client_secret (str): Secret do client
            
        Returns:
            AppClient: Instância criada
        """
        try:
            from accounts.models import Aplicacao
            from django.contrib.auth.hashers import make_password
            
            # Busca ou cria a aplicação
            app, _ = Aplicacao.objects.get_or_create(
                codigointerno=self.app_code,
                defaults={
                    'nomeaplicacao': 'Ações PNGI',
                    'isshowinportal': True
                }
            )
            
            # Cria o client
            client = AppClient.objects.create(
                aplicacao=app,
                client_id=client_id,
                client_secret_hash=make_password(client_secret),
                is_active=True
            )
            
            logger.info(f"App Client criado: {client_id}")
            return client
            
        except Exception as e:
            logger.error(f"Erro ao criar app client: {str(e)}")
            return None


# Instância singleton do serviço
portal_auth_service = PortalAuthService()
