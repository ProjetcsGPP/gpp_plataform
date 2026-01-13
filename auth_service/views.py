from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import User, UserRole, Attribute

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        permitions = User.get_all_permissions(user.email)
        
        # claims básicos
        token['useremail'] = user.email

        # aqui você pode, por enquanto, travar em uma empresa única
        roles = list(
            UserRole.objects.filter(user=user).values(
                'company__id', 'application__code', 'role__code'
            )
        )
        token['roles'] = roles

        # atributos ABAC simplificados
        attrs = list(
            Attribute.objects.filter(user=user).values(
                'company__id', 'application__code', 'key', 'value'
            )
        )
        token['attrs'] = attrs
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

