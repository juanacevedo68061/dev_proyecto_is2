from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Permission
from administracion.models import Categoria
from roles.models import Rol
from login.models import Usuario

class AdministracionViewsTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(username='testuser', password='testpassword')
        self.rol_administrador = Rol.objects.create(nombre='administrador')
        self.usuario.roles.add(self.rol_administrador)
        self.client.login(username='testuser', password='testpassword')
        self.categoria = Categoria.objects.create(nombre='Categoría de Prueba')


    def test_panel_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('administracion:panel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administracion/panel.html')

    def test_listar_categorias_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('administracion:listar_categorias'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administracion/listar_categorias.html')

    def test_crear_categoria_view(self):
        self.client.login(username='admin', password='password')
        data = {'nombre': 'Nueva Categoría'}
        response = self.client.post(reverse('administracion:crear_categoria'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Categoria.objects.filter(nombre='Nueva Categoría').exists())

    def test_editar_categoria_view(self):
        self.client.login(username='admin', password='password')
        data = {'nombre': 'Categoría Actualizada'}
        response = self.client.post(reverse('administracion:editar_categoria', args=[self.categoria.id]), data)
        self.assertEqual(response.status_code, 302)
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.nombre, 'Categoría Actualizada')

    def test_eliminar_categoria_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('administracion:eliminar_categoria', args=[self.categoria.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Categoria.objects.filter(nombre='Categoría de Prueba').exists())

    def test_gestion_usuarios_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('administracion:gestion_usuarios'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administracion/gestion_usuarios.html')

    def test_eliminar_usuario_view(self):
        usuario_a_eliminar = Usuario.objects.create_user(username='usuarioparaeliminar', password='password')
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('administracion:eliminar_usuario', args=[usuario_a_eliminar.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Usuario.objects.filter(username='usuarioparaeliminar').exists())

    def test_asignar_roles_usuario_view(self):
        rol_prueba = Rol.objects.create(nombre='autor')
        self.client.login(username='testuser', password='testpassword')
        data = {'roles': [rol_prueba.id]}
        response = self.client.post(reverse('administracion:asignar_roles_usuario', args=[self.usuario.id]), data)
        self.assertEqual(response.status_code, 302)
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.roles.filter(nombre='autor').exists())

    def test_eliminar_roles_usuario_view(self):
        usuario_a_editar = Usuario.objects.create_user(username='usuarioaeditar', password='password')
        usuario_a_editar.roles.add(self.rol_administrador)
        self.client.login(username='admin', password='password')
        data = {'roles': [self.rol_administrador.id]}
        response = self.client.post(reverse('administracion:eliminar_roles_usuario', args=[usuario_a_editar.id]), data)
        self.assertEqual(response.status_code, 302)
        usuario_a_editar.refresh_from_db()
        self.assertFalse(usuario_a_editar.roles.filter(nombre='administrador').exists())

    def test_agregar_permisos_roles_usuario_view(self):
        usuario_a_editar = Usuario.objects.create_user(username='usuarioaeditar', password='password')
        usuario_a_editar.roles.add(self.rol_administrador)
        self.client.login(username='admin', password='password')
        data = {
            'rol': self.rol_administrador.id,
            'permisos': ['permiso1'],
        }
        response = self.client.post(reverse('administracion:agregar_permisos_roles_usuario', args=[usuario_a_editar.id]), data)
        self.assertEqual(response.status_code, 200)
        usuario_a_editar.refresh_from_db()
        self.assertTrue(usuario_a_editar.roles.filter(permisos__codename='permiso1').exists())

    def test_eliminar_permisos_roles_usuario_view(self):
        usuario_a_editar = Usuario.objects.create_user(username='usuarioaeditar', password='password')
        self.rol_administrador.permisos.add(Permission.objects.get(codename='permiso1'))
        usuario_a_editar.roles.add(self.rol_administrador)
        self.client.login(username='admin', password='password')
        data = {'permisos': [Permission.objects.get(codename='permiso1').id]}
        response = self.client.post(reverse('administracion:eliminar_permisos_roles_usuario', args=[usuario_a_editar.id]), data)
        self.assertEqual(response.status_code, 302)
        usuario_a_editar.refresh_from_db()
        self.assertFalse(self.rol_administrador.permisos.filter(codename='permiso1').exists())
    