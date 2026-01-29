# accounts/views.py (ADICIONAR)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Aplicacao, Role, UserRole, User
from ..serializers import UserManagementSerializer  # Criar

class UserManagementView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = UserManagementSerializer(data=request.data)
        if serializer.is_valid():
            cpf = serializer.validated_data['cpf']
            role_codigo = serializer.validated_data['role_codigo_aplicacao']
            app_codigo = serializer.validated_data['aplicacao_destino']
            
            # Buscar/crir usuário
            user, created = User.objects.get_or_create(
                username=cpf,
                defaults={'first_name': serializer.validated_data['nome']}
            )
            
            # Role específica da app
            role = Role.objects.get(
                codigoperfil=role_codigo,
                aplicacaoid__codigointerno=app_codigo
            )
            
            # Atribuir role
            UserRole.objects.get_or_create(
                userid=user,
                roleid=role,
                aplicacaoid=role.aplicacaoid
            )
            
            # Token JWT para app (SimpleJWT)
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'userid': user.id,
                'access_token': str(refresh.access_token),
                'aplicacao': app_codigo
            })
        return Response(serializer.errors, status=400)
