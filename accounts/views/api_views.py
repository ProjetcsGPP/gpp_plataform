# accounts/views/api_views.py
"""
API Views do módulo Accounts (IAM).
Gerenciamento de usuários e autenticação JWT.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth import authenticate
import logging

from ..models import Aplicacao, Role, UserRole, User
from ..serializers import UserManagementSerializer
from ..services.token_service import (
    get_token_service,
    InvalidTokenException,
    UserRoleNotFoundException,
    TokenServiceException
)

logger = logging.getLogger(__name__)


# ============================================================================
# GESTÃO DE USUÁRIOS (MANTER EXISTENTE)
# ============================================================================

class UserManagementView(APIView):
    """
    View para gestão de usuários (MANTIDA DO CÓDIGO ORIGINAL).
    
    POST /api/gestao/usuarios/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = UserManagementSerializer(data=request.data)
        if serializer.is_valid():
            cpf = serializer.validated_data['cpf']
            role_codigo = serializer.validated_data['role_codigo_aplicacao']
            app_codigo = serializer.validated_data['aplicacao_destino']
            
            # Buscar/criar usuário
            user, created = User.objects.get_or_create(
                username=cpf,
                defaults={'first_name': serializer.validated_data['nome']}
            )
            
            # Role específica da app
            role = Role.objects.get(
                codigoperfil=role_codigo,
                aplicacao__codigointerno=app_codigo
            )
            
            # Atribuir role
            UserRole.objects.get_or_create(
                user=user,
                role=role,
                aplicacao=role.aplicacao
            )
            
            # ✨ NOVO: Usa TokenService ao invés de SimpleJWT
            token_service = get_token_service()
            
            try:
                access_token = token_service.issue_access_token(
                    user, app_codigo, role.id
                )
                
                return Response({
                    'user_id': user.id,
                    'access_token': access_token,
                    'aplicacao': app_codigo,
                    'role': role_codigo
                })
            except (UserRoleNotFoundException, TokenServiceException) as e:
                return Response(
                    {'detail': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================================================
# AUTENTICAÇÃO JWT (NOVAS VIEWS)
# ============================================================================


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        app_code = request.data.get('app_code')  # ✅ NOVO
        role_id = request.data.get('role_id')    # ✅ NOVO
        
        if not all([email, password, app_code, role_id]):
            return Response(
                {'error': 'Email, senha, app_code e role_id são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        token_service = get_token_service()
        
        result = token_service.login(email, password, app_code, role_id)
        
        if result:
            return Response({
                'user': {
                    'id': result['user'].id,
                    'email': result['user'].email,
                    'name': getattr(result['user'], 'name', ''),
                },
                'access_token': result['access_token'],
                'refresh_token': result['refresh_token'],
                'expires_in': result['expires_in'],
            })
        else:
            return Response(
                {'error': 'Credenciais inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class RefreshTokenView(APIView):
    """
    Renovação de tokens JWT.
    
    POST /api/auth/refresh/
    Body:
        {
            "refresh_token": "eyJ..."
        }
    
    Response:
        {
            "access_token": "eyJ...",
            "refresh_token": "eyJ..."
        }
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response(
                {'detail': 'refresh_token é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        token_service = get_token_service()
        
        try:
            tokens = token_service.refresh(refresh_token)
            
            logger.info("Tokens renovados com sucesso")
            
            return Response({
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token'],
                'token_type': 'Bearer',
                'expires_in': 600
            }, status=status.HTTP_200_OK)
        
        except InvalidTokenException as e:
            logger.warning(f"Tentativa de refresh com token inválido: {str(e)}")
            return Response(
                {'detail': str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        except Exception as e:
            logger.error(f"Erro inesperado no refresh: {str(e)}")
            return Response(
                {'detail': 'Erro ao renovar tokens'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    """
    Logout e revogação de tokens.
    
    POST /api/auth/logout/
    Headers:
        Authorization: Bearer <access_token>
    Body:
        {
            "refresh_token": "eyJ..."  // opcional
        }
    
    Response:
        {
            "detail": "Logout realizado com sucesso"
        }
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Extrai access token do header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        access_token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else None
        
        # Extrai refresh token do body
        refresh_token = request.data.get('refresh_token')
        
        token_service = get_token_service()
        revoked_count = 0
        
        # Revoga access token
        if access_token:
            try:
                token_service.revoke_token(access_token, is_refresh=False)
                revoked_count += 1
                logger.info(f"Access token revogado: user={request.user.email}")
            except InvalidTokenException as e:
                logger.warning(f"Erro ao revogar access token: {str(e)}")
        
        # Revoga refresh token
        if refresh_token:
            try:
                token_service.revoke_token(refresh_token, is_refresh=True)
                revoked_count += 1
                logger.info(f"Refresh token revogado: user={request.user.email}")
            except InvalidTokenException as e:
                logger.warning(f"Erro ao revogar refresh token: {str(e)}")
        
        if revoked_count == 0:
            return Response(
                {'detail': 'Nenhum token válido foi fornecido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {'detail': 'Logout realizado com sucesso'},
            status=status.HTTP_200_OK
        )


class ValidateTokenView(APIView):
    """
    Valida um access token e retorna informações do usuário.
    
    GET /api/auth/validate/
    Headers:
        Authorization: Bearer <access_token>
    
    Response:
        {
            "valid": true,
            "user": {
                "id": 1,
                "email": "usuario@example.com",
                "name": "Nome do Usuário"
            },
            "token_payload": {
                "sub": "1",
                "app_code": "ACOES_PNGI",
                "active_role_id": 5,
                "role_code": "GESTOR_PNGI",
                "exp": 1709035200,
                "iat": 1709034600
            }
        }
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Token já foi validado pelo middleware
        # Payload está disponível em request.token_payload
        
        token_payload = getattr(request, 'token_payload', None)
        
        return Response({
            'valid': True,
            'user': {
                'id': request.user.id,
                'email': request.user.email,
                'name': request.user.name,
                'is_active': request.user.is_active
            },
            'token_payload': token_payload
        }, status=status.HTTP_200_OK)


class ChangeRoleView(APIView):
    """
    Troca a role ativa do usuário na aplicação e emite novos tokens.
    
    POST /api/auth/change-role/
    Headers:
        Authorization: Bearer <access_token>
    Body:
        {
            "role_id": 5,
            "app_code": "ACOES_PNGI"  // opcional, usa do token atual
        }
    
    Response:
        {
            "access_token": "eyJ...",
            "refresh_token": "eyJ...",
            "user": {...},
            "message": "Role alterada com sucesso"
        }
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        role_id = request.data.get('role_id')
        
        # Pega app_code do token atual ou do body
        token_payload = getattr(request, 'token_payload', {})
        app_code = request.data.get('app_code', token_payload.get('app_code', 'ACOES_PNGI'))
        
        if not role_id:
            return Response(
                {'detail': 'role_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Valida se o usuário tem essa role na aplicação
        try:
            user_role = UserRole.objects.select_related(
                'role', 'aplicacao'
            ).get(
                user=request.user,
                role_id=role_id,
                aplicacao__codigointerno=app_code
            )
        except UserRole.DoesNotExist:
            return Response(
                {'detail': 'Role não encontrada ou usuário sem permissão'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Revoga tokens antigos
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            old_token = auth_header.replace('Bearer ', '')
            token_service = get_token_service()
            try:
                token_service.revoke_token(old_token, is_refresh=False)
            except InvalidTokenException:
                pass  # Token já pode estar expirado
        
        # Emite novos tokens com a nova role
        token_service = get_token_service()
        
        try:
            access_token = token_service.issue_access_token(
                request.user, app_code, role_id
            )
            refresh_token = token_service.issue_refresh_token(
                request.user, app_code, role_id
            )
            
            logger.info(
                f"Role alterada: user={request.user.email}, "
                f"new_role={user_role.role.codigoperfil}"
            )
            
            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer',
                'expires_in': 600,
                'user': {
                    'id': request.user.id,
                    'email': request.user.email,
                    'name': request.user.name,
                    'role': user_role.role.codigoperfil,
                    'app_code': app_code
                },
                'message': 'Role alterada com sucesso'
            }, status=status.HTTP_200_OK)
        
        except (UserRoleNotFoundException, TokenServiceException) as e:
            logger.error(f"Erro ao emitir tokens após mudança de role: {str(e)}")
            return Response(
                {'detail': 'Erro ao gerar novos tokens'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
