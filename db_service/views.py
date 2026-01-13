from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response

from db_service.auth import AppJWTAuthentication

class IsAppClient(BasePermission):
    def has_permission(self, request, view):
        token = getattr(request, 'auth', None)
        if not token:
            return False
        return 'app_code' in token

class GetPatriarcaView(APIView):
    authentication_classes = [AppJWTAuthentication]
    permission_classes = [IsAppClient]

    def get(self, request, patriarca_id):
        # Ler TBLPatriarca etc. e retornar JSON
        ...
        return Response(...)