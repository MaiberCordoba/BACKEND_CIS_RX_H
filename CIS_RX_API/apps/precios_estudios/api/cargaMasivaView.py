# apps/precios_estudios/api/cargaMasivaView.py (agrega esta nueva clase)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from ..models import Estudio

class CargaMasivaEstudiosJSONView(APIView):
    permission_classes = [IsAuthenticated]
    
    

    def post(self, request):
        estudios_data = request.data.get('estudios', [])
        print("request.data:", request.data)
        print("request.content_type:", request.content_type)
        if not estudios_data:
            return Response({'error': 'No se enviaron datos'}, status=400)

        count_creados = 0
        count_actualizados = 0
        batch = []
        batch_size = 200

        try:
            with transaction.atomic():
                for item in estudios_data:
                    batch.append(item)
                    if len(batch) >= batch_size:
                        for estudio_item in batch:
                            estudio, created = Estudio.objects.update_or_create(
                                codigo=estudio_item.get('codigo'),
                                defaults={
                                    'nombre': estudio_item.get('nombre', ''),
                                    'precio_particular': estudio_item.get('precio_particular', 0),
                                    'precio_medicos': estudio_item.get('precio_medicos', 0),
                                    'precio_previred': estudio_item.get('precio_previred', 0),
                                    'precio_plan_paciente_frecuente': estudio_item.get('precio_plan_paciente_frecuente', 0),
                                }
                            )
                            if created:
                                count_creados += 1
                            else:
                                count_actualizados += 1
                        batch = []
                
                # Procesar el resto
                for estudio_item in batch:
                    estudio, created = Estudio.objects.update_or_create(
                        codigo=estudio_item.get('codigo'),
                        defaults={
                            'nombre': estudio_item.get('nombre', ''),
                            'precio_particular': estudio_item.get('precio_particular', 0),
                            'precio_medicos': estudio_item.get('precio_medicos', 0),
                            'precio_previred': estudio_item.get('precio_previred', 0),
                            'precio_plan_paciente_frecuente': estudio_item.get('precio_plan_paciente_frecuente', 0),
                        }
                    )
                    if created:
                        count_creados += 1
                    else:
                        count_actualizados += 1

            return Response({
                'mensaje': 'Carga masiva completada',
                'creados': count_creados,
                'actualizados': count_actualizados,
                'total': count_creados + count_actualizados
            }, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=500)