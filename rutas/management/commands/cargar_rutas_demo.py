from datetime import datetime, time, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from rutas.models import Horario, Ruta


class Command(BaseCommand):
    help = 'Crea rutas y horarios ficticios para demostración.'

    def handle(self, *args, **options):
        terminales = [
            (
                'Rampa Pargua (Calbuco)',
                'Rampa Chacao (Ancud)',
                '0.5',
                1000,
            ),
            (
                'Rampa Chacao (Ancud)',
                'Terminal Embarcadero Hornopirén (Hualaihué)',
                '1.5',
                1500,
            ),
        ]
        fecha_salida = timezone.localdate() + timedelta(days=1)
        horarios_creados = 0

        for origen, destino, duracion, precio in terminales:
            ruta, creada = Ruta.objects.get_or_create(
                origen=origen,
                destino=destino,
                defaults={
                    'duracion_horas': duracion,
                    'precio_base': precio,
                    'activa': True,
                    'es_demostracion': True,
                },
            )

            if not creada and not ruta.es_demostracion:
                self.stdout.write(self.style.WARNING(
                    f'Se omitió la ruta existente no demo: {ruta}'
                ))
                continue

            if not ruta.horarios.filter(salida__gte=timezone.now()).exists():
                for hora_salida in (time(9, 0), time(15, 0)):
                    salida = timezone.make_aware(
                        datetime.combine(fecha_salida, hora_salida)
                    )
                    _, creada_horario = Horario.objects.get_or_create(
                        ruta=ruta,
                        salida=salida,
                        defaults={'activo': True},
                    )
                    horarios_creados += int(creada_horario)

        self.stdout.write(self.style.SUCCESS(
            f'Datos demo listos. Salidas nuevas: {horarios_creados}. '
            'Son ficticias y no corresponden a horarios reales.'
        ))