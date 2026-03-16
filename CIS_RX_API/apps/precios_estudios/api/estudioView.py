from rest_framework import viewsets, filters
from ..models import Estudio
from .estudioSerializer import EstudioSerializer

class EstudioModelViewSet(viewsets.ModelViewSet):
    queryset = Estudio.objects.all().order_by('nombre')
    serializer_class = EstudioSerializer
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'codigo']