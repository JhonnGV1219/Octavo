from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),

    path("provincias/", views.provincia_list, name="showProvincia"),
    path("provincias/nueva/", views.provincia_create, name="nuevaProvincia"),
    path("provincias/guardar/", views.provincia_create, name="guardarProvincia"),
    path("provincias/editar/<int:pk>/", views.provincia_edit, name="editarProvincia"),
    path("provincias/actualizar/", views.procesarActualizacionProvincia, name="procesarActualizacionProvincia"),
    path("provincias/eliminar/<int:pk>/", views.provincia_delete, name="eliminarProvincia"),
    path("provincias/<int:pk>/", views.provincia_detail, name="detalleProvincia"),

    path("cantones/", views.canton_list, name="showCanton"),
    path("cantones/nuevo/", views.canton_create, name="nuevoCanton"),
    path("cantones/guardar/", views.canton_create, name="guardarCanton"),
    path("cantones/editar/<int:pk>/", views.canton_edit, name="editarCanton"),
    path("cantones/actualizar/", views.procesarActualizacionCanton, name="procesarActualizacionCanton"),
    path("cantones/eliminar/<int:pk>/", views.canton_delete, name="eliminarCanton"),
    path("cantones/<int:pk>/", views.canton_detail, name="detalleCanton"),

    path("estudiantes/", views.estudiante_list, name="showEstudiante"),
    path("estudiantes/nuevo/", views.estudiante_create, name="nuevoEstudiante"),
    path("estudiantes/guardar/", views.estudiante_create, name="guardarEstudiante"),
    path("estudiantes/editar/<int:pk>/", views.estudiante_edit, name="editarEstudiante"),
    path("estudiantes/actualizar/", views.procesarActualizacionEstudiante, name="procesarActualizacionEstudiante"),
    path("estudiantes/eliminar/<int:pk>/", views.estudiante_delete, name="eliminarEstudiante"),
    path("estudiantes/<int:pk>/", views.estudiante_detail, name="detalleEstudiante"),

    path("universidades/", views.universidad_list, name="showUniversidad"),
    path("universidades/nueva/", views.universidad_create, name="nuevaUniversidad"),
    path("universidades/editar/<int:pk>/", views.universidad_edit, name="editarUniversidad"),
    path("universidades/eliminar/<int:pk>/", views.universidad_delete, name="eliminarUniversidad"),
    path("universidades/<int:pk>/", views.universidad_detail, name="detalleUniversidad"),
]
