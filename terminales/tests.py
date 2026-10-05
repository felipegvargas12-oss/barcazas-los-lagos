from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Terminal


class TerminalesTests(TestCase):
	def setUp(self):
		self.admin_user = User.objects.create_superuser(
			username='admin-terminales',
			password='test-password',
			email='admin-terminales@example.com',
		)

	def terminal_data(self, **overrides):
		data = {
			'nombre': 'Rampa de prueba',
			'comuna': 'Comuna de prueba',
			'estado': 'Operativa',
			'marea': 'Pleamar (Alta)',
			'_save': 'Save',
		}
		data.update(overrides)
		return data

	def test_public_page_shows_empty_state_and_terminals(self):
		url = reverse('terminales:lista')
		self.assertContains(
			self.client.get(url),
			'No hay terminales ni rampas registradas todavía.',
		)

		Terminal.objects.create(
			nombre='Rampa Pargua',
			comuna='Calbuco',
			estado='Operativa',
			marea='Pleamar (Alta)',
		)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Rampa Pargua')
		self.assertContains(response, 'Calbuco')
		self.assertContains(response, 'Pleamar (Alta)')
		terminal = Terminal.objects.get(nombre='Rampa Pargua')
		self.assertContains(response, reverse('terminales:detalle', args=[terminal.pk]))
		self.assertNotContains(response, 'Editar')
		self.assertNotContains(response, 'Eliminar')

	def test_terminal_detail_shows_map_for_known_location(self):
		call_command('cargar_terminales_demo')
		terminales_demo = Terminal.objects.filter(es_demostracion=True)
		self.assertEqual(terminales_demo.count(), 3)

		for terminal in terminales_demo:
			with self.subTest(terminal=terminal.nombre):
				response = self.client.get(
					reverse('terminales:detalle', args=[terminal.pk])
				)
				self.assertEqual(response.status_code, 200)
				self.assertContains(response, 'id="terminal-map"')

		hornopiren = Terminal.objects.get(nombre='Terminal Embarcadero Hornopirén')
		hornopiren_response = self.client.get(
			reverse('terminales:detalle', args=[hornopiren.pk])
		)
		self.assertContains(
			hornopiren_response,
			'no una ubicación verificada del embarcadero',
		)

	def test_terminal_detail_without_coordinates_shows_explanation(self):
		terminal = Terminal.objects.create(
			nombre='Terminal sin coordenadas',
			comuna='Comuna de prueba',
			estado='Operativa',
			marea='Sin información',
		)

		response = self.client.get(reverse('terminales:detalle', args=[terminal.pk]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'No hay coordenadas registradas para este terminal.')

	def test_missing_terminal_detail_returns_404(self):
		response = self.client.get(reverse('terminales:detalle', args=[999999]))

		self.assertEqual(response.status_code, 404)

	def test_demo_command_matches_route_terminal_names_and_is_idempotent(self):
		call_command('cargar_terminales_demo')
		call_command('cargar_terminales_demo')

		self.assertEqual(Terminal.objects.filter(es_demostracion=True).count(), 3)
		self.assertTrue(Terminal.objects.filter(
			nombre='Rampa Pargua', comuna='Calbuco'
		).exists())
		self.assertTrue(Terminal.objects.filter(
			nombre='Rampa Chacao', comuna='Ancud'
		).exists())
		self.assertTrue(Terminal.objects.filter(
			nombre='Terminal Embarcadero Hornopirén', comuna='Hualaihué'
		).exists())

	def test_admin_creates_terminal_and_public_page_displays_it(self):
		self.client.force_login(self.admin_user)
		response = self.client.post(
			reverse('admin:terminales_terminal_add'),
			self.terminal_data(),
		)

		self.assertEqual(response.status_code, 302)
		self.assertTrue(Terminal.objects.filter(nombre='Rampa de prueba').exists())
		self.assertContains(
			self.client.get(reverse('terminales:lista')),
			'Rampa de prueba',
		)

	def test_admin_rejects_missing_required_fields(self):
		self.client.force_login(self.admin_user)
		response = self.client.post(
			reverse('admin:terminales_terminal_add'),
			self.terminal_data(nombre=''),
		)

		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context['adminform'].form.errors)
		self.assertEqual(Terminal.objects.count(), 0)

	def test_admin_rejects_values_containing_only_symbols(self):
		self.client.force_login(self.admin_user)
		url = reverse('admin:terminales_terminal_add')
		for campo in ('nombre', 'comuna', 'estado', 'marea'):
			with self.subTest(campo=campo):
				response = self.client.post(url, self.terminal_data(**{campo: '!!!@@@'}))
				self.assertEqual(response.status_code, 200)
				self.assertIn(campo, response.context['adminform'].form.errors)
		self.assertEqual(Terminal.objects.count(), 0)

	def test_admin_edits_and_deletes_terminal(self):
		terminal = Terminal.objects.create(
			nombre='Rampa anterior',
			comuna='Comuna anterior',
			estado='Operativa',
			marea='Pleamar (Alta)',
		)
		self.client.force_login(self.admin_user)
		response = self.client.post(
			reverse('admin:terminales_terminal_change', args=[terminal.pk]),
			self.terminal_data(nombre='Rampa actualizada'),
		)

		self.assertEqual(response.status_code, 302)
		terminal.refresh_from_db()
		self.assertEqual(terminal.nombre, 'Rampa actualizada')

		delete_url = reverse('admin:terminales_terminal_delete', args=[terminal.pk])
		self.assertEqual(self.client.get(delete_url).status_code, 200)
		self.assertTrue(Terminal.objects.filter(pk=terminal.pk).exists())
		delete_response = self.client.post(delete_url, {'post': 'yes'})
		self.assertEqual(delete_response.status_code, 302)
		self.assertFalse(Terminal.objects.filter(pk=terminal.pk).exists())
