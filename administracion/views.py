from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria
from .forms import CategoriaForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from roles.decorators import rol_requerido

@rol_requerido('administrador')
@login_required
def panel(request):
    """
    Vista para el panel de administración.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.

    Retorna:
        HttpResponse: Redirecciona a la vista del panel de administración principal.
    """
    # Tu lógica para el panel principal va aquí
    return render(request, 'administracion/panel.html')

@rol_requerido('administrador')
@login_required
def listar_categorias(request):
    """
    Vista para listar categorías.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.

    Retorna:
        HttpResponse: Muestra la lista de categorías.
    """
    categorias = Categoria.objects.all()
    return render(request, 'administracion/listar_categorias.html', {'categorias': categorias})

@rol_requerido('administrador')
@login_required
def crear_categoria(request):
    """
    Vista para crear una nueva categoría.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.

    Retorna:
        HttpResponse: Redirecciona a la vista de lista de categorías si la categoría se crea con éxito,
        o muestra el formulario de creación de categoría con errores.
    """
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'La categoría se ha creado correctamente.')
            return redirect('administracion:listar_categorias')
        else:
            messages.error(request, 'Hubo un problema al crear la categoría. Por favor, verifica los datos ingresados.')
    else:
        form = CategoriaForm()

    return render(request, 'administracion/crear_categoria.html', {'form': form})

@rol_requerido('administrador')
@login_required
def editar_categoria(request, categoria_id):
    """
    Vista para editar una categoría existente.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.
        categoria_id (int): El ID de la categoría que se va a editar.

    Retorna:
        HttpResponse: Redirecciona a la vista de lista de categorías si la categoría se edita con éxito,
        o muestra el formulario de edición de categoría con errores.
    """
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'La categoría se ha actualizado correctamente.')
            return redirect('administracion:listar_categorias')
        else:
            messages.error(request, 'Hubo un problema al actualizar la categoría. Por favor, verifica los datos ingresados.')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'administracion/editar_categoria.html', {'form': form, 'categoria': categoria})

@rol_requerido('administrador')
@login_required
def eliminar_categoria(request, categoria_id):
    """
    Vista para eliminar una categoría existente.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.
        categoria_id (int): El ID de la categoría que se va a eliminar.

    Retorna:
        HttpResponse: Redirecciona a la vista de lista de categorías si la categoría se elimina con éxito,
        o muestra la confirmación de eliminación de categoría con errores.
    """
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'La categoría se ha eliminado correctamente.')
        return redirect('administracion:listar_categorias')
    return render(request, 'administracion/eliminar_categoria.html', {'categoria': categoria})


