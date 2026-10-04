from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Horario, Ruta


class RutasViewsTests(TestCase):
	def setUp(self):
		self.ruta = Ruta.objects.create(
			origen='Puerto Montt',
			destino='Chaiten',
			duracion_horas='4.5',
			precio_base=10000,
		)
		self.staff = User.objects.create_user(
			username='gestor',
			password='test-password',
			is_staff=True,
			is_superuser=True,
		)

	def test_public_can_consult_routes_and_future_departures(self):
		salida = timezone.now() + timedelta(days=1)
		Horario.objects.create(ruta=self.ruta, salida=salida)

		response = self.client.get(reverse('rutas:horarios'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Puerto Montt')
		self.assertContains(response, 'Chaiten')
		self.assertContains(
			response,
			timezone.localtime(salida).strftime('%d/%m/%Y %H:%M'),
		)
		self.assertContains(response, reverse('rutas:detalle', args=[self.ruta.pk]))

	def test_route_detail_displays_map_for_demo_terminals(self):
		call_command('cargar_rutas_demo')
		ruta_demo = Ruta.objects.get(origen='Rampa Pargua (Calbuco)')

		response = self.client.get(reverse('rutas:detalle', args=[ruta_demo.pk]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'id="route-map"')
		self.assertContains(response, '-41.7927842')
		self.assertContains(response, 'no representa una ruta real de navegación')
		self.assertNotContains(response, 'El punto de Hornopirén es referencial')

		ruta_hornopiren = Ruta.objects.get(
			destino='Terminal Embarcadero Hornopirén (Hualaihué)'
		)
		hornopiren_response = self.client.get(
			reverse('rutas:detalle', args=[ruta_hornopiren.pk])
		)
		self.assertContains(
			hornopiren_response,
			'El punto de Hornopirén es referencial',
		)

	def test_public_does_not_see_inactive_or_past_departures(self):
		pasada = timezone.now() - timedelta(days=1)
		Horario.objects.create(ruta=self.ruta, salida=pasada)
		Horario.objects.create(
			ruta=self.ruta,
			salida=timezone.now() + timedelta(days=1),
			activo=False,
		)

		response = self.client.get(reverse('rutas:horarios'))

		self.assertContains(response, 'No hay salidas programadas.')

	def test_demo_command_uses_terminal_names_and_is_idempotent(self):
		call_command('cargar_rutas_demo')
		call_command('cargar_rutas_demo')

		rutas_demo = Ruta.objects.filter(es_demostracion=True)
		self.assertEqual(rutas_demo.count(), 2)
		self.assertEqual(
			Horario.objects.filter(ruta__in=rutas_demo).count(),
			4,
		)
		self.assertTrue(rutas_demo.filter(
			origen='Rampa Pargua (Calbuco)',
			destino='Rampa Chacao (Ancud)',
		).exists())
		self.assertTrue(rutas_demo.filter(
			destino='Terminal Embarcadero Hornopirén (Hualaihué)',
		).exists())

	def test_route_management_controls_are_not_shown_on_public_page(self):
		self.client.force_login(self.staff)
		response = self.client.get(reverse('rutas:horarios'))

		self.assertNotContains(response, 'Nueva Ruta')
		self.assertNotContains(response, 'Editar ruta')
		self.assertNotContains(response, 'Eliminar ruta')
		self.assertNotContains(response, 'Agregar salida')

	def test_staff_manages_routes_and_schedules_in_admin(self):
		self.client.force_login(self.staff)

		for view_name in (
			'admin:rutas_ruta_changelist',
			'admin:rutas_horario_changelist',
		):
			response = self.client.get(reverse(view_name))
			self.assertEqual(response.status_code, 200)
