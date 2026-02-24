# accounts/services/token_service.py
"""
TokenService Centralizado para IAM
Implementa JWT com HS256 para monolito Django com tokens contextuais por aplicação.
"""

import uuid
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import jwt
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

from accounts.models import User, UserRole, Aplicacao

logger = logging.getLogger(__name__)


class TokenServiceException(Exception):
    """Exceção base para erros do TokenService"""
    pass


class InvalidTokenException(TokenServiceException):
    """Token inválido ou expirado"""
    pass


class UserRoleNotFoundException(TokenServiceException):
    """UserRole não encontrado ou inativo"""
    pass


class TokenService:
    """
    Serviço centralizado para gerenciamento de tokens JWT.
    
    Características:
    - JWT com HS256 (monolito)
    - Access token: 10 minutos
    - Refresh token: 30 minutos
    - Token contextual por aplicação
    - Claims: sub, app_code, active_role_id, exp, jti
    - Suporte a blacklist futura via cache/database
    """
    
    # Configurações de tempo de vida dos tokens
    ACCESS_TOKEN_LIFETIME = timedelta(minutes=10)
    REFRESH_TOKEN_LIFETIME = timedelta(minutes=30)
    
    # Algoritmo de assinatura
    ALGORITHM = 'HS256'
    
    # Prefixos para cache de blacklist
    BLACKLIST_PREFIX = 'token_blacklist:'
    REFRESH_BLACKLIST_PREFIX = 'refresh_blacklist:'
    
    def __init__(self):
        """Inicializa o TokenService com a chave secreta do Django"""
        self.secret_key = settings.SECRET_KEY
        
        if not self.secret_key or len(self.secret_key) < 50:
            logger.warning(
                "SECRET_KEY muito curta. Use uma chave de pelo menos 50 caracteres "
                "para produção. Gere uma com: python -c 'from django.core.management.utils "
                "import get_random_secret_key; print(get_random_secret_key())'"
            )
    
    # Em accounts/services/token_service.py
    def login(self, username_or_email: str, password: str):
        """
        Autentica usuário e retorna token_data compatível com web/API.
        Retorna: {'user': user, 'payload': payload, 'token': token} ou None
        """
        # Tenta username ou email (comum no seu projeto)
        user = authenticate(username=username_or_email, password=password)
        if not user or not user.is_active:
            return None
        
        # Gera payload JWT customizado (roles, etc.)
        payload = self._generate_payload(user)  # Implemente baseado no seu JWT encoder
        
        # Armazena active role se necessário
        # self.set_active_role(user.id, role_id)  # Opcional
        
        logger.info(f"Token gerado para {user.email}")
        return {
            'user': user,
            'payload': payload,
            'token': self._encode_jwt(payload)  # Seu método de encode JWT
        }
        
    
    def _generate_jti(self) -> str:
        """
        Gera um JTI (JWT ID) único e seguro.
        
        Estratégia:
        - UUID4 (aleatório e único)
        - Timestamp para ordenação temporal
        - Combina unicidade + auditoria temporal
        
        Returns:
            str: JTI único no formato 'uuid4-timestamp'
        """
        unique_id = uuid.uuid4().hex
        timestamp = int(timezone.now().timestamp())
        return f"{unique_id}-{timestamp}"
    
    def _get_blacklist_key(self, jti: str, is_refresh: bool = False) -> str:
        """
        Gera chave de cache para blacklist.
        
        Args:
            jti: JWT ID
            is_refresh: Se é refresh token
            
        Returns:
            str: Chave de cache
        """
        prefix = self.REFRESH_BLACKLIST_PREFIX if is_refresh else self.BLACKLIST_PREFIX
        return f"{prefix}{jti}"
    
    def _is_blacklisted(self, jti: str, is_refresh: bool = False) -> bool:
        """
        Verifica se um token está na blacklist.
        
        Args:
            jti: JWT ID
            is_refresh: Se é refresh token
            
        Returns:
            bool: True se está na blacklist
        """
        key = self._get_blacklist_key(jti, is_refresh)
        return cache.get(key) is not None
    
    def blacklist_token(self, jti: str, exp: datetime, is_refresh: bool = False) -> None:
        """
        Adiciona um token à blacklist.
        
        Estratégia:
        - Cache Redis/Memcached para performance
        - TTL automático igual ao tempo restante do token
        - Não armazena tokens expirados (economia de memória)
        
        Args:
            jti: JWT ID
            exp: Data de expiração do token
            is_refresh: Se é refresh token
        """
        now = timezone.now()
        
        # Não adiciona tokens já expirados
        if exp <= now:
            logger.debug(f"Token {jti} já expirado, não adicionado à blacklist")
            return
        
        # Calcula TTL (tempo até expiração)
        ttl_seconds = int((exp - now).total_seconds())
        
        key = self._get_blacklist_key(jti, is_refresh)
        
        # Armazena no cache com TTL
        cache.set(
            key,
            {
                'blacklisted_at': now.isoformat(),
                'expires_at': exp.isoformat(),
                'is_refresh': is_refresh
            },
            timeout=ttl_seconds
        )
        
        logger.info(
            f"Token {'refresh' if is_refresh else 'access'} {jti} "
            f"adicionado à blacklist (TTL: {ttl_seconds}s)"
        )
    
    def issue_access_token(
        self,
        user: User,
        app_code: str,
        role_id: int,
        extra_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Emite um access token JWT.
        
        Args:
            user: Instância do usuário
            app_code: Código da aplicação (ex: 'ACOES_PNGI')
            role_id: ID da role ativa
            extra_claims: Claims adicionais opcionais
            
        Returns:
            str: Access token JWT
            
        Raises:
            UserRoleNotFoundException: Se UserRole não existe ou está inativo
        """
        # Valida se UserRole existe e está ativo
        try:
            user_role = UserRole.objects.select_related(
                'user', 'aplicacao', 'role'
            ).get(
                user=user,
                aplicacao__codigointerno=app_code,
                role_id=role_id
            )
        except UserRole.DoesNotExist:
            raise UserRoleNotFoundException(
                f"UserRole não encontrado: user={user.id}, "
                f"app={app_code}, role={role_id}"
            )
        
        # Valida se usuário está ativo
        if not user.is_active:
            raise TokenServiceException(f"Usuário {user.id} está inativo")
        
        now = timezone.now()
        exp = now + self.ACCESS_TOKEN_LIFETIME
        jti = self._generate_jti()
        
        # Claims padrão
        payload = {
            'sub': str(user.id),  # Subject: user_id
            'app_code': app_code,  # Código da aplicação
            'active_role_id': role_id,  # ID da role ativa
            'role_code': user_role.role.codigoperfil,  # Código da role (ex: GESTOR_PNGI)
            'exp': int(exp.timestamp()),  # Expiration time
            'iat': int(now.timestamp()),  # Issued at
            'jti': jti,  # JWT ID (único)
            'token_type': 'access'  # Tipo de token
        }
        
        # Adiciona claims extras
        if extra_claims:
            payload.update(extra_claims)
        
        # Gera o token
        token = jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.ALGORITHM
        )
        
        logger.info(
            f"Access token emitido: user={user.id}, app={app_code}, "
            f"role={user_role.role.codigoperfil}, jti={jti}"
        )
        
        return token
    
    def issue_refresh_token(
        self,
        user: User,
        app_code: str,
        role_id: int,
        extra_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Emite um refresh token JWT.
        
        Args:
            user: Instância do usuário
            app_code: Código da aplicação
            role_id: ID da role ativa
            extra_claims: Claims adicionais opcionais
            
        Returns:
            str: Refresh token JWT
            
        Raises:
            UserRoleNotFoundException: Se UserRole não existe ou está inativo
        """
        # Valida se UserRole existe
        try:
            user_role = UserRole.objects.select_related(
                'user', 'aplicacao', 'role'
            ).get(
                user=user,
                aplicacao__codigointerno=app_code,
                role_id=role_id
            )
        except UserRole.DoesNotExist:
            raise UserRoleNotFoundException(
                f"UserRole não encontrado: user={user.id}, "
                f"app={app_code}, role={role_id}"
            )
        
        # Valida se usuário está ativo
        if not user.is_active:
            raise TokenServiceException(f"Usuário {user.id} está inativo")
        
        now = timezone.now()
        exp = now + self.REFRESH_TOKEN_LIFETIME
        jti = self._generate_jti()
        
        # Claims padrão
        payload = {
            'sub': str(user.id),
            'app_code': app_code,
            'active_role_id': role_id,
            'role_code': user_role.role.codigoperfil,
            'exp': int(exp.timestamp()),
            'iat': int(now.timestamp()),
            'jti': jti,
            'token_type': 'refresh'  # Tipo de token
        }
        
        # Adiciona claims extras
        if extra_claims:
            payload.update(extra_claims)
        
        # Gera o token
        token = jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.ALGORITHM
        )
        
        logger.info(
            f"Refresh token emitido: user={user.id}, app={app_code}, "
            f"role={user_role.role.codigoperfil}, jti={jti}"
        )
        
        return token
    
    def validate_access_token(self, token: str) -> Dict[str, Any]:
        """
        Valida um access token JWT.
        
        Validações:
        1. Assinatura válida
        2. Não expirado
        3. Não está na blacklist
        4. UserRole ainda existe
        5. Usuário ainda está ativo
        6. Aplicação ainda está ativa
        
        Args:
            token: Token JWT
            
        Returns:
            Dict: Payload do token decodificado
            
        Raises:
            InvalidTokenException: Se token inválido
        """
        try:
            # Decodifica o token
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.ALGORITHM],
                options={'verify_exp': True}
            )
        except jwt.ExpiredSignatureError:
            raise InvalidTokenException("Token expirado")
        except jwt.InvalidTokenError as e:
            raise InvalidTokenException(f"Token inválido: {str(e)}")
        
        # Verifica tipo de token
        if payload.get('token_type') != 'access':
            raise InvalidTokenException("Token não é um access token")
        
        # Verifica blacklist
        jti = payload.get('jti')
        if not jti:
            raise InvalidTokenException("Token sem JTI")
        
        if self._is_blacklisted(jti, is_refresh=False):
            raise InvalidTokenException("Token revogado (blacklist)")
        
        # Valida UserRole
        user_id = payload.get('sub')
        app_code = payload.get('app_code')
        role_id = payload.get('active_role_id')
        
        try:
            user_role = UserRole.objects.select_related(
                'user', 'aplicacao', 'role'
            ).get(
                user_id=user_id,
                aplicacao__codigointerno=app_code,
                role_id=role_id
            )
        except UserRole.DoesNotExist:
            raise InvalidTokenException(
                "UserRole não existe mais ou foi desativado"
            )
        
        # Valida usuário ativo
        if not user_role.user.is_active:
            raise InvalidTokenException("Usuário inativo")
        
        logger.debug(f"Access token válido: jti={jti}, user={user_id}")
        
        return payload
    
    def refresh(self, refresh_token: str) -> Dict[str, str]:
        """
        Gera novos tokens a partir de um refresh token.
        
        Validações:
        1. Refresh token válido
        2. Não expirado
        3. Não está na blacklist
        4. UserRole ainda existe
        5. Usuário ainda está ativo
        6. Aplicação ainda está ativa
        7. Role ainda pertence ao usuário
        
        Comportamento:
        - Gera novo access token
        - Gera novo refresh token
        - Adiciona refresh token antigo à blacklist (rotation)
        
        Args:
            refresh_token: Refresh token JWT
            
        Returns:
            Dict com 'access_token' e 'refresh_token'
            
        Raises:
            InvalidTokenException: Se refresh token inválido
        """
        try:
            # Decodifica o refresh token
            payload = jwt.decode(
                refresh_token,
                self.secret_key,
                algorithms=[self.ALGORITHM],
                options={'verify_exp': True}
            )
        except jwt.ExpiredSignatureError:
            raise InvalidTokenException("Refresh token expirado")
        except jwt.InvalidTokenError as e:
            raise InvalidTokenException(f"Refresh token inválido: {str(e)}")
        
        # Verifica tipo de token
        if payload.get('token_type') != 'refresh':
            raise InvalidTokenException("Token não é um refresh token")
        
        # Verifica blacklist
        jti = payload.get('jti')
        if not jti:
            raise InvalidTokenException("Token sem JTI")
        
        if self._is_blacklisted(jti, is_refresh=True):
            raise InvalidTokenException("Refresh token revogado (blacklist)")
        
        # Extrai informações
        user_id = payload.get('sub')
        app_code = payload.get('app_code')
        role_id = payload.get('active_role_id')
        
        # Valida UserRole ainda existe
        try:
            user_role = UserRole.objects.select_related(
                'user', 'aplicacao', 'role'
            ).get(
                user_id=user_id,
                aplicacao__codigointerno=app_code,
                role_id=role_id
            )
        except UserRole.DoesNotExist:
            raise InvalidTokenException(
                "UserRole não existe mais. Faça login novamente."
            )
        
        # Valida usuário ativo
        if not user_role.user.is_active:
            raise InvalidTokenException("Usuário inativo")
        
        # Valida aplicação ativa (se houver campo de status)
        # if not user_role.aplicacao.is_active:
        #     raise InvalidTokenException("Aplicação inativa")
        
        # Adiciona refresh token antigo à blacklist (rotation)
        exp_datetime = datetime.fromtimestamp(
            payload['exp'],
            tz=timezone.get_current_timezone()
        )
        self.blacklist_token(jti, exp_datetime, is_refresh=True)
        
        # Gera novos tokens
        new_access_token = self.issue_access_token(
            user_role.user,
            app_code,
            role_id
        )
        
        new_refresh_token = self.issue_refresh_token(
            user_role.user,
            app_code,
            role_id
        )
        
        logger.info(
            f"Tokens renovados: user={user_id}, app={app_code}, "
            f"old_jti={jti}"
        )
        
        return {
            'access_token': new_access_token,
            'refresh_token': new_refresh_token
        }
    
    def revoke_token(self, token: str, is_refresh: bool = False) -> None:
        """
        Revoga um token adicionando-o à blacklist.
        
        Args:
            token: Token JWT
            is_refresh: Se é refresh token
            
        Raises:
            InvalidTokenException: Se token inválido
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.ALGORITHM],
                options={'verify_exp': False}  # Permite revogar tokens expirados
            )
        except jwt.InvalidTokenError as e:
            raise InvalidTokenException(f"Token inválido: {str(e)}")
        
        jti = payload.get('jti')
        if not jti:
            raise InvalidTokenException("Token sem JTI")
        
        exp_datetime = datetime.fromtimestamp(
            payload['exp'],
            tz=timezone.get_current_timezone()
        )
        
        self.blacklist_token(jti, exp_datetime, is_refresh)
        
        logger.info(f"Token revogado manualmente: jti={jti}")
    
    def revoke_all_user_tokens(self, user_id: int, app_code: Optional[str] = None) -> int:
        """
        Revoga todos os tokens de um usuário.
        
        Estratégia para implementação futura:
        - Incrementar um contador de versão no User
        - Adicionar 'token_version' aos claims
        - Rejeitar tokens com versão antiga na validação
        
        Args:
            user_id: ID do usuário
            app_code: Código da aplicação (opcional, None = todas)
            
        Returns:
            int: Número de tokens revogados (implementação futura)
        """
        # TODO: Implementar com campo User.token_version
        logger.warning(
            f"revoke_all_user_tokens não implementado ainda. "
            f"Use User.token_version para invalidação global. "
            f"user_id={user_id}, app_code={app_code}"
        )
        return 0


# Instância singleton
_token_service = None


def get_token_service() -> TokenService:
    """
    Retorna instância singleton do TokenService.
    
    Returns:
        TokenService: Instância única
    """
    global _token_service
    if _token_service is None:
        _token_service = TokenService()
    return _token_service
