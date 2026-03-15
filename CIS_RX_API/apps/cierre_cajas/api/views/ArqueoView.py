from rest_framework.viewsets import ModelViewSet;
from ...models import Arqueo
from ..seriliazers.arqueoSerializer import ArqueoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ArqueoModelViewSet(ModelViewSet):
    queryset = Arqueo.objects.all().order_by('-id')
    serializer_class = ArqueoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    