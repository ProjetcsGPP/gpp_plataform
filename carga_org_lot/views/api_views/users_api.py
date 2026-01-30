"""
Users API - Gerenciamento de Usuários
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import User, AppRoleAssignment
from ...permissions import IsGestor
from common.models import TblAplicacao

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
        return TblAplicacao.objects.get(str_sigla_aplicacao='CARGA_ORG_LOT')
    
    @action(detail=False, methods=['get'], url_path='list_users')
    def list_users(self, request):
        """
        Lista todos os usuários com acesso ao app.
        
        **URL:** `GET /api/v1/carga/users/list_users/`
        """
        try:
            app = self.get_app()
            
            # Busca todos os assignments do app
            assignments = AppRoleAssignment.objects.filter(
                fk_aplicacao=app
            ).select_related('fk_user', 'fk_role')
            
            users_data = []
            for assignment in assignments:
                users_data.append({
                    'id': assignment.fk_user.id_user,
                    'email': assignment.fk_user.str_email,
                    'name': assignment.fk_user.str_nome,
                    'role': assignment.fk_role.str_nome_role,
                    'role_code': assignment.fk_role.str_sigla_role,
                    'is_active': assignment.fk_user.is_active,
                    'assigned_at': assignment.dat_criacao,
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
            user = User.objects.get(str_email=email)
            app = self.get_app()
            
            # Busca assignment
            try:
                assignment = AppRoleAssignment.objects.get(
                    fk_user=user,
                    fk_aplicacao=app
                )
                role = assignment.fk_role.str_sigla_role
                role_name = assignment.fk_role.str_nome_role
                assigned_at = assignment.dat_criacao
            except AppRoleAssignment.DoesNotExist:
                role = None
                role_name = None
                assigned_at = None
            
            user_data = {
                'id': user.id_user,
                'email': user.str_email,
                'name': user.str_nome,
                'role': role_name,
                'role_code': role,
                'is_active': user.is_active,
                'assigned_at': assigned_at,
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
                str_email=email,
                defaults={
                    'str_nome': request.data.get('name', email),
                }
            )
            
            if not created and request.data.get('name'):
                user.str_nome = request.data.get('name')
                user.save()
            
            logger.info(
                f"Usuário {'criado' if created else 'atualizado'}: {email}"
            )
            
            return Response(
                {
                    'message': f"Usuário {'criado' if created else 'atualizado'} com sucesso",
                    'user_id': user.id_user,
                    'email': user.str_email,
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar usuário: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Erro ao sincronizar usuário'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
