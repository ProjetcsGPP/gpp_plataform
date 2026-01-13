from rest_framework_simplejwt.authentication import JWTAuthentication

class AppJWTAuthentication(JWTAuthentication):
    """
    Variante separada para tokens de aplicação.
    """
    def get_user(self, validated_token):
        # pode retornar um objeto "fake user" ou None;
        # o importante é validar claims como 'app_code'
        return None