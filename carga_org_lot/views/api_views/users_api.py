"""
Users API - Gerenciamento de Usuários
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import User, UserRole, Aplicacao
from ...permissions import IsGestor

import logging

logger = logging.getLogger(__name__)


class UserManagementViewSet(viewsets.ViewSet):
    """
    ViewSet para gerenciamento de usuários do app CARGA_ORG_LOT.
    
    Apenas Gestores têm acesso.
    """
    permission_classes = [IsAuthenticated, IsGestor]
    lookup_field = 'email'
    
    def get_app(self):
        """Retorna a aplicação CARGA_ORG_LOT."""
        return Aplicacao.objects.get(codigointerno='CARGA_ORG_LOT')
    
    @action(detail=False, methods=['get'], url_path='list_users')
    def list_users(self, request):
        """
        Lista todos os usuários com acesso ao app.
        
        **URL:** `GET /api/v1/carga/users/list_users/`
        """
        try:
            app = self.get_app()
            
            # Busca todos os UserRole do app
            user_roles = UserRole.objects.filter(
                aplicacao=app
            ).select_related('user', 'role')
            
            users_data = []
            for ur in user_roles:
                users_data.append({
                    'id': ur.user.id,
                    'email': ur.user.email,
                    'name': ur.user.name,
                    'role': ur.role.nomeperfil,
                    'role_code': ur.role.codigoperfil,
                    'is_active': ur.user.is_active,
                })
            
            logger.info(f"Lista de {len(users_data)} usuários retornada")
            return Response(users_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Erro ao listar usuários: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Erro ao listar usuários'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, email=None):
        """
        Busca um usuário específico por email.
        
        **URL:** `GET /api/v1/carga/users/{email}/`
        """
        try:
            user = User.objects.get(email=email)
            app = self.get_app()
            
            # Busca UserRole
            try:
                user_role = UserRole.objects.get(
                    user=user,
                    aplicacao=app
                )
                role = user_role.role.codigoperfil
                role_name = user_role.role.nomeperfil
            except UserRole.DoesNotExist:
                role = None
                role_name = None
            
            user_data = {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'role': role_name,
                'role_code': role,
                'is_active': user.is_active,
            }
            
            return Response(user_data, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response(
                {'error': 'Usuário não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Erro ao buscar usuário: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Erro ao buscar usuário'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], url_path='sync_user')
    def sync_user(self, request):
        """
        Sincroniza usuário do Portal com o app.
        
        Usado para adicionar/atualizar permissões de um usuário.
        
        **URL:** `POST /api/v1/carga/users/sync_user/`
        
        **Body:**
        ```json
        {
            "email": "user@example.com",
            "name": "Nome do Usuário",
            "roles": ["GESTOR_CARGA"],
            "attributes": {"can_upload": "true"}
        }
        ```
        """
        try:
            email = request.data.get('email')
            if not email:
                return Response(
                    {'error': 'Email é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Busca ou cria usuário
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'name': request.data.get('name', email),
                }
            )
            
            if not created and request.data.get('name'):
                user.name = request.data.get('name')
                user.save()
            
            logger.info(
                f"Usuário {'criado' if created else 'atualizado'}: {email}"
            )
            
            return Response(
                {
                    'message': f"Usuário {'criado' if created else 'atualizado'} com sucesso",
                    'user_id': user.id,
                    'email': user.email,
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar usuário: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Erro ao sincronizar usuário'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
