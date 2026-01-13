from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .permissions import CanManageCarga

class UploadOrganogramaView(APIView):
    permission_classes = [CanManageCarga]

    def post(self, request):
        # receber arquivo, criar OrganogramaVersao, etc.
        return Response({'status': 'ok'})


@api_view(['GET'])
@permission_classes([CanManageCarga])
def carga_home(request):
    """
    Entrada da aplicação de carga de organograma/lotação.
    Só deixa entrar se o JWT tiver role/atributo corretos.
    """
    user = request.user
    return Response({
        'message': 'Bem-vindo à Carga de Organograma/Lotação',
        'user': user.email,
    })    