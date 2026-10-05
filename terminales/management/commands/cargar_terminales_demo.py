from django.core.management.base import BaseCommand

from terminales.models import Terminal


class Command(BaseCommand):
    help = 'Carga terminales y rampas ficticios para demostración.'

    def handle(self, *args, **options):
        terminales_demo = [
            {
                'nombre': 'Rampa Pargua',
                'comuna': 'Calbuco',
                'marea': 'Pleamar (Alta)',
                'estado': 'Operativa',
            },
            {
                'nombre': 'Rampa Chacao',
                'comuna': 'Ancud',
                'marea': 'Pleamar (Alta)',
                'estado': 'Operativa',
            },
            {
                'nombre': 'Terminal Embarcadero Hornopirén',
                'comuna': 'Hualaihué',
                'marea': 'Bajamar (Baja)',
                'estado': 'Precaución por rampa seca',
            },
        ]
        creados = 0
        for datos in terminales_demo:
            _, creado = Terminal.objects.get_or_create(
                nombre=datos['nombre'],
                comuna=datos['comuna'],
                defaults={
                    'marea': datos['marea'],
                    'estado': datos['estado'],
                    'es_demostracion': True,
                },
            )
            creados += int(creado)

        self.stdout.write(self.style.SUCCESS(
            f'Terminales demo listos. Registros nuevos: {creados}. '
            'La información es ficticia y no indica condiciones actuales.'
        ))