from django.test import TestCase
from django.urls import reverse
from login.models import Usuario
from roles.models import Rol
from administracion.models import Categoria
class AdministracionFunctionalTestCase(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(username='testuser', password='testpassword')
        self.rol_administrador = Rol.objects.create(nombre='administrador')
        self.usuario.roles.add(self.rol_administrador)
        self.client.login(username='testuser', password='testpassword')

    def test_panel_url(self):
        url = reverse('administracion:panel')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_listar_categorias_url(self):
        url = reverse('administracion:listar_categorias')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_crear_categoria_url(self):
        url = reverse('administracion:crear_categoria')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_editar_categoria_url(self):
        categoria = Categoria.objects.create(nombre='Categoria de Prueba')
        url = reverse('administracion:editar_categoria', args=[categoria.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_eliminar_categoria_url(self):
        categoria = Categoria.objects.create(nombre='Categoria de Prueba')
        url = reverse('administracion:eliminar_categoria', args=[categoria.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_gestion_usuarios_url(self):
        url = reverse('administracion:gestion_usuarios')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_asignar_roles_usuario_url(self):
        usuario = Usuario.objects.create_user(username='testuser2', password='testpassword')
        url = reverse('administracion:asignar_roles_usuario', args=[usuario.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_eliminar_roles_usuario_url(self):
        usuario = Usuario.objects.create_user(username='testuser2', password='testpassword')
        url = reverse('administracion:eliminar_roles_usuario', args=[usuario.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_eliminar_usuario_url(self):
        usuario = Usuario.objects.create_user(username='testuser2', password='testpassword')
        url = reverse('administracion:eliminar_usuario', args=[usuario.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_agregar_permisos_roles_usuario_url(self):
        usuario = Usuario.objects.create_user(username='testuser2', password='testpassword')
        url = reverse('administracion:agregar_permisos_roles_usuario', args=[usuario.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_eliminar_permisos_roles_usuario_url(self):
        usuario = Usuario.objects.create_user(username='testuser2', password='testpassword')
        url = reverse('administracion:eliminar_permisos_roles_usuario', args=[usuario.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

