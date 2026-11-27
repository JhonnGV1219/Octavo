
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .models import TbProvincia, TbCanton, TbEstudiantes


# ==========================================
# INICIO
# ==========================================

def inicio(request):
    return render(request, 'principal/inicio.html')


# ==========================================
# CRUD PROVINCIAS
# ==========================================

# Mostrar formulario para nueva provincia
def nuevaProvincia(request):
    return render(request, 'provincias/newprovincia.html')


# Guardar provincia
def guardarProvincia(request):

    id_provincia = request.POST['id_provincia']
    nombre = request.POST['nombre_provincia']

    TbProvincia.objects.create(
        id_provincia=id_provincia,
        nombre_provincia=nombre
    )

    messages.success(request, 'Provincia agregada exitosamente')
    return redirect('/provincias')


# Mostrar listado de provincias
def showProvincia(request):

    provincias = TbProvincia.objects.all()

    return render(request, 'provincias/showprovincia.html',
                  {'misProvincias': provincias})


# Mostrar formulario de edición
def editarProvincia(request, id):

    provincia = get_object_or_404(TbProvincia, id_provincia=id)

    return render(request, 'provincias/editprovincia.html',
                  {'miProvincia': provincia})


# Procesar actualización
def procesarActualizacionProvincia(request):

    id = request.POST['id_provincia']
    nombre = request.POST['nombre_provincia']

    provincia = get_object_or_404(TbProvincia, id_provincia=id)

    provincia.nombre_provincia = nombre
    provincia.save()

    messages.success(request, 'Provincia actualizada exitosamente')
    return redirect('/provincias')


# Eliminar provincia
def eliminarProvincia(request, id):

    provincia = get_object_or_404(TbProvincia, id_provincia=id)
    provincia.delete()

    messages.success(request, 'Provincia eliminada exitosamente')
    return redirect('/provincias')


# ==========================================
# CRUD CANTONES
# ==========================================

# Mostrar formulario de nuevo cantón
def nuevoCanton(request):

    provincias = TbProvincia.objects.all()

    return render(request, 'canton/newcanton.html',
                  {'misProvincias': provincias})


# Guardar cantón
def guardarCanton(request):

    nombre = request.POST['nombre_canton']
    provincia = request.POST['id_provincia']

    TbCanton.objects.create(
        nombre_canton=nombre,
        id_provincia_id=provincia
    )

    messages.success(request, 'Cantón agregado exitosamente')
    return redirect('/cantones')


# Mostrar listado de cantones
def showCanton(request):

    cantones = TbCanton.objects.select_related('id_provincia').all()

    return render(request, 'canton/showcanton.html',
                  {'misCantones': cantones})


# Mostrar formulario de edición
def editarCanton(request, id):

    canton = get_object_or_404(TbCanton, id_canton=id)
    provincias = TbProvincia.objects.all()

    return render(request, 'canton/editcanton.html',
                  {
                      'miCanton': canton,
                      'misProvincias': provincias
                  })


# Procesar actualización
def procesarActualizacionCanton(request):

    id = request.POST['id_canton']
    nombre = request.POST['nombre_canton']
    provincia = request.POST['id_provincia']

    canton = get_object_or_404(TbCanton, id_canton=id)

    canton.nombre_canton = nombre
    canton.id_provincia_id = provincia

    canton.save()

    messages.success(request, 'Cantón actualizado exitosamente')
    return redirect('/cantones')


# Eliminar cantón
def eliminarCanton(request, id):

    canton = get_object_or_404(TbCanton, id_canton=id)
    canton.delete()

    messages.success(request, 'Cantón eliminado exitosamente')
    return redirect('/cantones')


# ==========================================
# CRUD ESTUDIANTES
# ==========================================

# Mostrar formulario de nuevo estudiante
def nuevoEstudiante(request):

    cantones = TbCanton.objects.all()

    return render(request, 'estudiantes/newestudiante.html',
                  {'misCantones': cantones})


# Guardar estudiante
def guardarEstudiante(request):

    apellido = request.POST['apellido_est']
    nombre = request.POST['nombre_est']
    cedula = request.POST['cedula_est']
    canton = request.POST['id_canton']
    direccion = request.POST['direccion_est']
    fecha = request.POST['fecha_nacimiento_est']
    estado = request.POST['estado_est']

    TbEstudiantes.objects.create(
        apellido_est=apellido,
        nombre_est=nombre,
        cedula_est=cedula,
        id_canton_id=canton,
        direccion_est=direccion,
        fecha_nacimiento_est=fecha,
        fecha_creacion_est=timezone.now(),
        fecha_actualizacion_est=timezone.now(),
        estado_est=estado
    )

    messages.success(request, 'Estudiante agregado exitosamente')
    return redirect('/estudiantes')


# Mostrar listado de estudiantes
def showEstudiante(request):

    estudiantes = TbEstudiantes.objects.select_related(
        'id_canton',
        'id_canton__id_provincia'
    ).all()

    return render(request, 'estudiantes/showestudiante.html',
                  {'misEstudiantes': estudiantes})


# Mostrar formulario de edición
def editarEstudiante(request, id):

    estudiante = get_object_or_404(TbEstudiantes, id_est=id)
    cantones = TbCanton.objects.all()

    return render(request, 'estudiantes/editestudiante.html',
                  {
                      'miEstudiante': estudiante,
                      'misCantones': cantones
                  })


# Procesar actualización
def procesarActualizacionEstudiante(request):

    id = request.POST['id_est']
    apellido = request.POST['apellido_est']
    nombre = request.POST['nombre_est']
    cedula = request.POST['cedula_est']
    canton = request.POST['id_canton']
    direccion = request.POST['direccion_est']
    fecha = request.POST['fecha_nacimiento_est']
    estado = request.POST['estado_est']

    estudiante = get_object_or_404(TbEstudiantes, id_est=id)

    estudiante.apellido_est = apellido
    estudiante.nombre_est = nombre
    estudiante.cedula_est = cedula
    estudiante.id_canton_id = canton
    estudiante.direccion_est = direccion
    estudiante.fecha_nacimiento_est = fecha
    estudiante.fecha_actualizacion_est = timezone.now()
    estudiante.estado_est = estado

    estudiante.save()

    messages.success(request, 'Estudiante actualizado exitosamente')
    return redirect('/estudiantes')


# Eliminar estudiante
def eliminarEstudiante(request, id):

    estudiante = get_object_or_404(TbEstudiantes, id_est=id)
    estudiante.delete()

    messages.success(request, 'Estudiante eliminado exitosamente')
    return redirect('/estudiantes')
