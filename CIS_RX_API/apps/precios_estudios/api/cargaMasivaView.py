import pandas as pd
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from ..models import Estudio

class CargaMasivaEstudiosView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        archivo = request.FILES.get('archivo')
        if not archivo:
            return Response({'error': 'No se envió ningún archivo'}, status=status.HTTP_400_BAD_REQUEST)

        if not archivo.name.endswith(('.xlsx', '.xls')):
            return Response({'error': 'Formato no soportado. Use .xlsx o .xls'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(archivo)
            df.columns = df.columns.str.strip()

            count_creados = 0
            count_actualizados = 0

            with transaction.atomic():
                for _, row in df.iterrows():
                    estudio, created = Estudio.objects.update_or_create(
                        codigo=str(row['codigo']).strip(),
                        defaults={
                            'nombre': row['nombre'],
                            'precio_particular': row['precio_particular'],
                            'precio_medicos': row['precio_medicos'],
                            'precio_previred': row['precio_previred'],
                            'precio_plan_paciente_frecuente': row['precio_plan_paciente_frecuente'],
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
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)