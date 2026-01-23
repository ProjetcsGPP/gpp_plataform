"""
Serviço genérico de autenticação via portal.
Fornece funcionalidades reutilizáveis para autenticação e sincronização de usuários.
"""

import logging
import requests
from typing import Optional, Dict, List, Tuple, TYPE_CHECKING
from django.conf import settings
from django.db import transaction

# Imports condicionais para type hints (evita imports circulares)
if TYPE_CHECKING:
    from accounts.models import User, Aplicacao

logger = logging.getLogger(__name__)


class PortalAuthService:
    """
    Serviço genérico para autenticação via Portal.
    Cada aplicação pode instanciar este serviço com seu próprio APP_CODE.
    """
    
    def __init__(self, app_code: str):
        """
        Inicializa o serviço com o código da aplicação.
        
        Args:
            app_code: Código interno da aplicação (ex: 'PORTAL', 'CARGAORGLOT', 'ACOESPNGI')
        """
        self.app_code = app_code
        self.portal_url = getattr(settings, 'PORTAL_AUTH_URL', None)
        
        if not self.portal_url:
            logger.warning(f"[{self.app_code}] PORTAL_AUTH_URL não configurada")
    
    def authenticate_user(self, token: str) -> Optional['User']:
        """
        Autentica usuário via token do portal.
        
        Args:
            token: Token JWT do portal
            
        Returns:
            Instância do usuário autenticado ou None se falhar
        """
        from accounts.models import User
        
        try:
            # Valida token com o portal
            user_data = self._validate_token_with_portal(token)
            
            if not user_data:
                return None
            
            # Busca ou cria o usuário localmente
            email = user_data.get('email')
            if not email:
                logger.error(f"[{self.app_code}] Email não encontrado nos dados do portal")
                return None
            
            try:
                user = User.objects.get(email__iexact=email)
                logger.info(f"[{self.app_code}] Usuário encontrado: {email}")
                return user
            except User.DoesNotExist:
                logger.warning(f"[{self.app_code}] Usuário não encontrado localmente: {email}")
                return None
                
        except Exception as e:
            logger.error(f"[{self.app_code}] Erro na autenticação: {str(e)}")
            return None
    
    def _validate_token_with_portal(self, token: str) -> Optional[Dict]:
        """
        Valida token com o portal de autenticação.
        
        Args:
            token: Token JWT do portal
            
        Returns:
            Dados do usuário ou None se inválido
        """
        if not self.portal_url:
            # Modo desenvolvimento: retorna dados mockados
            logger.warning(f"[{self.app_code}] Modo desenvolvimento - validação mockada")
            return {
                'email': 'dev@example.com',
                'name': 'Desenvolvedor',
                'roles': [],
                'attributes': {}
            }
        
        try:
            response = requests.post(
                f"{self.portal_url}/api/auth/validate",
                json={'token': token},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    f"[{self.app_code}] Portal retornou status {response.status_code}"
                )
                return None
                
        except requests.RequestException as e:
            logger.error(f"[{self.app_code}] Erro ao conectar com portal: {str(e)}")
            return None
    
    def sync_user(
        self,
        email: str,
        name: str,
        roles_data: Optional[List[str]] = None,
        attributes_data: Optional[Dict[str, str]] = None
    ) -> Tuple['User', bool, 'Aplicacao']:
        """
        Sincroniza usuário com roles e atributos da aplicação.
        
        Args:
            email: Email do usuário
            name: Nome do usuário
            roles_data: Lista de códigos de roles (ex: ['GESTORCARGA'])
            attributes_data: Dicionário de atributos (ex: {'can_upload': 'true'})
            
        Returns:
            Tupla (usuário, created, aplicacao)
        """
        from accounts.models import User, Aplicacao, Role, UserRole, Attribute
        from django.contrib.auth.hashers import make_password
        
        roles_data = roles_data or []
        attributes_data = attributes_data or {}
        
        try:
            with transaction.atomic():
                # Busca a aplicação
                try:
                    app = Aplicacao.objects.get(codigointerno=self.app_code)
                except Aplicacao.DoesNotExist:
                    raise ValueError(
                        f"Aplicação '{self.app_code}' não encontrada. "
                        "Certifique-se de criar a aplicação no banco de dados."
                    )
                
                # Cria ou atualiza usuário
                user, created = User.objects.get_or_create(
                    email__iexact=email,
                    defaults={
                        'email': email,
                        'name': name,
                        'password': make_password(None),
                        'idstatususuario': 1,
                        'idtipousuario': 1,
                        'idclassificacaousuario': 1,
                        'is_active': True,
                    }
                )
                
                if not created:
                    # Atualiza nome se necessário
                    if user.name != name:
                        user.name = name
                        user.save(update_fields=['name'])
                
                # Sincroniza roles
                if roles_data:
                    self._sync_user_roles(user, app, roles_data)
                
                # Sincroniza atributos
                if attributes_data:
                    self._sync_user_attributes(user, app, attributes_data)
                
                logger.info(
                    f"[{self.app_code}] Usuário {'criado' if created else 'atualizado'}: "
                    f"{email}"
                )
                
                return user, created, app
                
        except Exception as e:
            logger.error(f"[{self.app_code}] Erro ao sincronizar usuário: {str(e)}")
            raise
    
    def _sync_user_roles(
        self,
        user: 'User',
        app: 'Aplicacao',
        role_codes: List[str]
    ) -> None:
        """
        Sincroniza roles do usuário para esta aplicação.
        
        Args:
            user: Instância do usuário
            app: Instância da aplicação
            role_codes: Lista de códigos de roles
        """
        from accounts.models import Role, UserRole
        
        # Remove roles anteriores desta aplicação
        UserRole.objects.filter(user=user, aplicacao=app).delete()
        
        # Adiciona novos roles
        for role_code in role_codes:
            try:
                role = Role.objects.get(
                    codigoperfil=role_code,
                    aplicacao=app
                )
                
                UserRole.objects.create(
                    user=user,
                    role=role,
                    aplicacao=app
                )
                
                logger.debug(
                    f"[{self.app_code}] Role '{role_code}' atribuída a {user.email}"
                )
                
            except Role.DoesNotExist:
                logger.warning(
                    f"[{self.app_code}] Role '{role_code}' não encontrada "
                    f"para aplicação '{app.codigointerno}'"
                )
    
    def _sync_user_attributes(
        self,
        user: 'User',
        app: 'Aplicacao',
        attributes: Dict[str, str]
    ) -> None:
        """
        Sincroniza atributos do usuário para esta aplicação.
        
        Args:
            user: Instância do usuário
            app: Instância da aplicação
            attributes: Dicionário de atributos
        """
        from accounts.models import Attribute
        
        for key, value in attributes.items():
            Attribute.objects.update_or_create(
                user=user,
                aplicacao=app,
                key=key,
                defaults={'value': str(value)}
            )
            
            logger.debug(
                f"[{self.app_code}] Atributo '{key}={value}' "
                f"definido para {user.email}"
            )
    
    def get_user_roles(self, email: str) -> List[Dict[str, str]]:
        """
        Retorna roles do usuário para esta aplicação.
        
        Args:
            email: Email do usuário
            
        Returns:
            Lista de dicionários com informações das roles
        """
        from accounts.models import User, UserRole
        
        try:
            user = User.objects.get(email__iexact=email)
            app = self._get_application()
            
            user_roles = UserRole.objects.filter(
                user=user,
                aplicacao=app
            ).select_related('role')
            
            return [
                {
                    'code': ur.role.codigoperfil,
                    'name': ur.role.nomeperfil,
                }
                for ur in user_roles
            ]
            
        except User.DoesNotExist:
            logger.warning(f"[{self.app_code}] Usuário não encontrado: {email}")
            return []
        except Exception as e:
            logger.error(f"[{self.app_code}] Erro ao buscar roles: {str(e)}")
            return []
    
    def get_user_attributes(self, email: str) -> Dict[str, str]:
        """
        Retorna atributos do usuário para esta aplicação.
        
        Args:
            email: Email do usuário
            
        Returns:
            Dicionário de atributos
        """
        from accounts.models import User, Attribute
        
        try:
            user = User.objects.get(email__iexact=email)
            app = self._get_application()
            
            attributes = Attribute.objects.filter(
                user=user,
                aplicacao=app
            )
            
            return {attr.key: attr.value for attr in attributes}
            
        except User.DoesNotExist:
            logger.warning(f"[{self.app_code}] Usuário não encontrado: {email}")
            return {}
        except Exception as e:
            logger.error(f"[{self.app_code}] Erro ao buscar atributos: {str(e)}")
            return {}
    
    def _get_application(self) -> 'Aplicacao':
        """Helper para obter a aplicação"""
        from accounts.models import Aplicacao
        return Aplicacao.objects.get(codigointerno=self.app_code)


# Cache de instâncias do serviço por APP_CODE
_service_instances: Dict[str, PortalAuthService] = {}


def get_portal_auth_service(app_code: str) -> PortalAuthService:
    """
    Factory para obter instância do serviço de autenticação.
    
    Args:
        app_code: Código da aplicação
        
    Returns:
        Instância do PortalAuthService
    """
    if app_code not in _service_instances:
        _service_instances[app_code] = PortalAuthService(app_code)
    
    return _service_instances[app_code]
