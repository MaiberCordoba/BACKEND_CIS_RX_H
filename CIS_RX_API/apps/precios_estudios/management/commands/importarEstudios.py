import pandas as pd
from django.core.management.base import BaseCommand
from ...models import Estudio
from django.db import transaction

class Command(BaseCommand):
    help = 'Importar estudios desde un archivo Excel'

    def add_arguments(self, parser):
        parser.add_argument('archivo', type=str, help='Ruta del archivo Excel (.xlsx)')

    def handle(self, *args, **options):
        ruta_archivo = options['archivo']

        try:
            df = pd.read_excel(ruta_archivo)
            
            df.columns = df.columns.str.strip()

            self.stdout.write(self.style.SUCCESS(f'Leyendo {len(df)} registros...'))

            count_creados = 0
            count_actualizados = 0

            with transaction.atomic():
                for index, row in df.iterrows():
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

            self.stdout.write(self.style.SUCCESS(
                f'¡Proceso terminado! Creados: {count_creados}, Actualizados: {count_actualizados}'
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al importar: {str(e)}'))