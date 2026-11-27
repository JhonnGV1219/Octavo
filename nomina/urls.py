
from django.urls import path
from . import views

urlpatterns = [

    # INICIO
    path('', views.inicio, name='inicio'),

    # PROVINCIAS
    path('provincias/nueva/', views.nuevaProvincia, name='nuevaProvincia'),
    path('provincias/guardar/', views.guardarProvincia, name='guardarProvincia'),
    path('provincias/', views.showProvincia, name='showProvincia'),
    path('provincias/editar/<int:id>/', views.editarProvincia, name='editarProvincia'),
    path('provincias/actualizar/', views.procesarActualizacionProvincia, name='procesarActualizacionProvincia'),
    path('provincias/eliminar/<int:id>/', views.eliminarProvincia, name='eliminarProvincia'),

    # CANTONES
    path('cantones/nuevo/', views.nuevoCanton, name='nuevoCanton'),
    path('cantones/guardar/', views.guardarCanton, name='guardarCanton'),
    path('cantones/', views.showCanton, name='showCanton'),
    path('cantones/editar/<int:id>/', views.editarCanton, name='editarCanton'),
    path('cantones/actualizar/', views.procesarActualizacionCanton, name='procesarActualizacionCanton'),
    path('cantones/eliminar/<int:id>/', views.eliminarCanton, name='eliminarCanton'),

    # ESTUDIANTES
    path('estudiantes/nuevo/', views.nuevoEstudiante, name='nuevoEstudiante'),
    path('estudiantes/guardar/', views.guardarEstudiante, name='guardarEstudiante'),
    path('estudiantes/', views.showEstudiante, name='showEstudiante'),
    path('estudiantes/editar/<int:id>/', views.editarEstudiante, name='editarEstudiante'),
    path('estudiantes/actualizar/', views.procesarActualizacionEstudiante, name='procesarActualizacionEstudiante'),
    path('estudiantes/eliminar/<int:id>/', views.eliminarEstudiante, name='eliminarEstudiante'),

]
