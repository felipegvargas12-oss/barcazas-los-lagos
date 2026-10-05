from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client, TestCase
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

	def test_admin_creates_route_visible_in_list_and_database(self):
		self.client.force_login(self.staff)
		response = self.client.post(
			reverse('admin:rutas_ruta_add'),
			{
				'origen': 'Rampa de prueba',
				'destino': 'Terminal de prueba',
				'duracion_horas': '2.5',
				'precio_base': '5000',
				'activa': 'on',
				'_save': 'Save',
			},
		)

		self.assertEqual(response.status_code, 302)
		ruta = Ruta.objects.get(origen='Rampa de prueba')
		self.assertEqual(ruta.destino, 'Terminal de prueba')
		self.assertContains(
			self.client.get(reverse('rutas:horarios')),
			'Rampa de prueba',
		)

	def test_admin_rejects_empty_and_invalid_route_data(self):
		self.client.force_login(self.staff)
		url = reverse('admin:rutas_ruta_add')
		valid_data = {
			'origen': 'Origen de prueba',
			'destino': 'Destino de prueba',
			'duracion_horas': '2.5',
			'precio_base': '5000',
			'activa': 'on',
			'_save': 'Save',
		}

		for invalid_data in (
			{**valid_data, 'origen': ''},
			{**valid_data, 'precio_base': '0'},
			{**valid_data, 'destino': 'Origen de prueba'},
		):
			with self.subTest(invalid_data=invalid_data):
				response = self.client.post(url, invalid_data)
				self.assertEqual(response.status_code, 200)
				self.assertFalse(Ruta.objects.filter(
					origen=invalid_data['origen'],
					destino=invalid_data['destino'],
				).exists())

	def test_admin_edits_route_and_persists_change(self):
		self.client.force_login(self.staff)
		response = self.client.post(
			reverse('admin:rutas_ruta_change', args=[self.ruta.pk]),
			{
				'origen': self.ruta.origen,
				'destino': 'Nuevo destino',
				'duracion_horas': '5.0',
				'precio_base': '12000',
				'activa': 'on',
				'es_demostracion': '',
				'_save': 'Save',
			},
		)

		self.assertEqual(response.status_code, 302)
		self.ruta.refresh_from_db()
		self.assertEqual(self.ruta.destino, 'Nuevo destino')
		self.assertEqual(self.ruta.precio_base, 12000)

	def test_admin_delete_confirmation_can_be_cancelled_or_confirmed(self):
		self.client.force_login(self.staff)
		url = reverse('admin:rutas_ruta_delete', args=[self.ruta.pk])

		cancel_response = self.client.get(url)
		self.assertEqual(cancel_response.status_code, 200)
		self.assertTrue(Ruta.objects.filter(pk=self.ruta.pk).exists())

		delete_response = self.client.post(url, {'post': 'yes'})
		self.assertEqual(delete_response.status_code, 302)
		self.assertFalse(Ruta.objects.filter(pk=self.ruta.pk).exists())

	def test_admin_returns_404_for_missing_route(self):
		response = self.client.get(
			reverse('rutas:detalle', args=[999999])
		)

		self.assertEqual(response.status_code, 404)

	def test_admin_rejects_missing_csrf_and_accepts_valid_token(self):
		client = Client(enforce_csrf_checks=True)
		client.force_login(self.staff)
		url = reverse('admin:rutas_ruta_add')
		form_response = client.get(url)
		csrf_token = client.cookies['csrftoken'].value
		data = {
			'origen': 'CSRF origen',
			'destino': 'CSRF destino',
			'duracion_horas': '1.0',
			'precio_base': '1000',
			'activa': 'on',
			'_save': 'Save',
		}

		self.assertEqual(form_response.status_code, 200)
		self.assertEqual(client.post(url, data).status_code, 403)

		data['csrfmiddlewaretoken'] = csrf_token
		valid_response = client.post(url, data)
		self.assertEqual(valid_response.status_code, 302)
		self.assertTrue(Ruta.objects.filter(origen='CSRF origen').exists())
