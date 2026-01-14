from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import User, UserRole, Attribute

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        permissions = User.get_all_permissions(user)
        
        # DEBUG: Print para verificar o conteúdo
        #print("=" * 50)
        #print(f"DEBUG - Usuário: {user.email}")
        #print(f"DEBUG - Tipo de permissions: {type(permissions)}")
        #print(f"DEBUG - Permissions: {permissions}")
        #print("=" * 50)
        
        # Claims básicos
        token['useremail'] = user.email
        token['username'] = user.name
        token['permissions'] = list(permissions)
        
        # Roles RBAC por aplicação
        roles = list(
            UserRole.objects.filter(user=user).values(
                'aplicacao__codigointerno', 
                'role__codigoperfil',
                'role__nomeperfil'
            )
        )
        
        #print(f"DEBUG - Roles: {roles}")
        
        token['roles'] = roles
        
        # Atributos ABAC simplificados
        attrs = list(
            Attribute.objects.filter(user=user).values(
                'aplicacao__codigointerno', 
                'key', 
                'value'
            )
        )
        
        #print(f"DEBUG - Attrs: {attrs}")
        #print("=" * 50)
        
        token['attrs'] = attrs
        
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

