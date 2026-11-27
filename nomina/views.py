from django.contrib import messages
from django.db import DatabaseError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CantonForm, EstudianteForm, ProvinciaForm, UniversidadForm
from .models import TbCanton, TbEstudiantes, TbProvincia, TbUniversidades


ENTITY = {
    "provincia": {
        "model": TbProvincia, "form": ProvinciaForm, "label": "Provincia", "plural": "Provincias",
        "list_name": "showProvincia", "queryset": lambda: TbProvincia.objects.all().order_by("nombre_provincia"),
        "search": lambda q: Q(nombre_provincia__icontains=q),
        "values": lambda o: [o.id_provincia, o.nombre_provincia or "—"],
        "headers": ["Código", "Provincia"],
        "details": lambda o: [("Código", o.id_provincia), ("Nombre", o.nombre_provincia or "—")],
        "key": lambda o: o.id_provincia,
    },
    "canton": {
        "model": TbCanton, "form": CantonForm, "label": "Cantón", "plural": "Cantones",
        "list_name": "showCanton", "queryset": lambda: TbCanton.objects.select_related("id_provincia").order_by("nombre_canton"),
        "search": lambda q: Q(nombre_canton__icontains=q) | Q(id_provincia__nombre_provincia__icontains=q),
        "values": lambda o: [o.id_canton, o.nombre_canton or "—", o.id_provincia.nombre_provincia if o.id_provincia else "Sin provincia"],
        "headers": ["Código", "Cantón", "Provincia"],
        "details": lambda o: [("Código", o.id_canton), ("Cantón", o.nombre_canton or "—"), ("Provincia", o.id_provincia.nombre_provincia if o.id_provincia else "Sin provincia")],
        "key": lambda o: o.id_canton,
    },
    "estudiante": {
        "model": TbEstudiantes, "form": EstudianteForm, "label": "Estudiante", "plural": "Estudiantes",
        "list_name": "showEstudiante", "queryset": lambda: TbEstudiantes.objects.select_related("id_canton", "id_canton__id_provincia").order_by("apellido_est", "nombre_est"),
        "search": lambda q: Q(apellido_est__icontains=q) | Q(nombre_est__icontains=q) | Q(cedula_est__icontains=q) | Q(id_canton__nombre_canton__icontains=q) | Q(id_canton__id_provincia__nombre_provincia__icontains=q),
        "values": lambda o: [o.id_est, f"{o.apellido_est} {o.nombre_est}", o.cedula_est, o.id_canton.nombre_canton if o.id_canton else "Sin cantón", o.id_canton.id_provincia.nombre_provincia if o.id_canton and o.id_canton.id_provincia else "Sin provincia", o.fecha_nacimiento_est.strftime("%d/%m/%Y"), o.estado_est or "—"],
        "headers": ["Código", "Estudiante", "Cédula", "Cantón", "Provincia", "Nacimiento", "Estado"],
        "details": lambda o: [("Código", o.id_est), ("Apellidos", o.apellido_est), ("Nombres", o.nombre_est), ("Cédula", o.cedula_est), ("Cantón", o.id_canton.nombre_canton if o.id_canton else "Sin cantón"), ("Provincia", o.id_canton.id_provincia.nombre_provincia if o.id_canton and o.id_canton.id_provincia else "Sin provincia"), ("Dirección", o.direccion_est), ("Fecha de nacimiento", o.fecha_nacimiento_est.strftime("%d/%m/%Y")), ("Estado", o.estado_est or "—"), ("Creado", o.fecha_creacion_est.strftime("%d/%m/%Y %H:%M") if o.fecha_creacion_est else "—"), ("Actualizado", o.fecha_actualizacion_est.strftime("%d/%m/%Y %H:%M") if o.fecha_actualizacion_est else "—")],
        "key": lambda o: o.id_est,
    },
    "universidad": {
        "model": TbUniversidades, "form": UniversidadForm, "label": "Universidad", "plural": "Universidades",
        "list_name": "showUniversidad", "queryset": lambda: TbUniversidades.objects.all().order_by("nombre_uni"),
        "search": lambda q: Q(nombre_uni__icontains=q) | Q(rector_uni__icontains=q) | Q(estado_uni__icontains=q),
        "values": lambda o: [o.id_uni, o.nombre_uni or "—", o.rector_uni or "—", o.estado_uni or "—"],
        "headers": ["Código", "Universidad", "Rector/a", "Estado"],
        "details": lambda o: [("Código", o.id_uni), ("Universidad", o.nombre_uni or "—"), ("Rector/a", o.rector_uni or "—"), ("Estado", o.estado_uni or "—"), ("Creada", o.creacion_uni.strftime("%d/%m/%Y %H:%M") if o.creacion_uni else "—"), ("Actualizada", o.actualizacion_uni.strftime("%d/%m/%Y %H:%M") if o.actualizacion_uni else "—")],
        "key": lambda o: o.id_uni,
    },
}


def entity_route(entity):
    return {"provincia": "provincias", "canton": "cantones", "estudiante": "estudiantes", "universidad": "universidades"}[entity]


def _get(entity, pk):
    model = ENTITY[entity]["model"]
    return get_object_or_404(model, **{model._meta.pk.name: pk})


def _list(request, entity):
    config = ENTITY[entity]
    query = request.GET.get("q", "").strip()[:100]
    queryset = config["queryset"]()
    if query:
        queryset = queryset.filter(config["search"](query))
    rows = []
    for obj in queryset:
        key = config["key"](obj)
        base = f"/{entity_route(entity)}"
        rows.append({
            "values": config["values"](obj),
            "detail_url": f"{base}/{key}/",
            "edit_url": f"{base}/editar/{key}/",
            "delete_url": f"{base}/eliminar/{key}/",
        })
    create_suffix = "nuevo" if entity in ("canton", "estudiante") else "nueva"
    return render(request, "principal/entity_list.html", {
        "entity": entity, "entity_label": config["label"], "entity_plural": config["plural"],
        "headers": config["headers"], "rows": rows, "query": query,
        "create_url": f"/{entity_route(entity)}/{create_suffix}/",
        "list_url": f"/{entity_route(entity)}/", "active_menu": entity,
    })


def _form(request, entity, pk=None):
    config = ENTITY[entity]
    instance = _get(entity, pk) if pk is not None else None
    data = request.POST if request.method == "POST" else None
    form = config["form"](data, instance=instance)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        now = timezone.now()
        if entity == "estudiante":
            if obj.fecha_creacion_est is None:
                obj.fecha_creacion_est = now
            obj.fecha_actualizacion_est = now
        elif entity == "universidad":
            if obj.creacion_uni is None:
                obj.creacion_uni = now
            obj.actualizacion_uni = now
        obj.save()
        messages.success(request, f"{config['label']} {'actualizada' if instance else 'registrada'} correctamente.")
        return redirect(config["list_name"])
    return render(request, "principal/entity_form.html", {
        "entity": entity, "entity_label": config["label"], "entity_plural": config["plural"],
        "form": form, "instance": instance, "is_edit": instance is not None,
        "list_url": f"/{entity_route(entity)}/", "active_menu": entity,
    })


def _detail(request, entity, pk):
    config = ENTITY[entity]
    obj = _get(entity, pk)
    if entity == "estudiante":
        obj = TbEstudiantes.objects.select_related("id_canton", "id_canton__id_provincia").get(pk=pk)
    elif entity == "canton":
        obj = TbCanton.objects.select_related("id_provincia").get(pk=pk)
    base = f"/{entity_route(entity)}"
    key = config["key"](obj)
    return render(request, "principal/entity_detail.html", {
        "entity": entity, "entity_label": config["label"], "entity_plural": config["plural"],
        "object": obj, "details": config["details"](obj),
        "list_url": f"{base}/", "edit_url": f"{base}/editar/{key}/",
        "delete_url": f"{base}/eliminar/{key}/", "active_menu": entity,
    })


@require_POST
def _delete(request, entity, pk):
    config = ENTITY[entity]
    obj = _get(entity, pk)
    try:
        obj.delete()
    except DatabaseError:
        messages.error(request, f"No se pudo eliminar {config['label'].lower()}: existen registros relacionados.")
    else:
        messages.success(request, f"{config['label']} eliminada correctamente.")
    return redirect(config["list_name"])


def _legacy_update(request, entity, pk_field):
    if request.method != "POST":
        return redirect(ENTITY[entity]["list_name"])
    return _form(request, entity, request.POST.get(pk_field))


def inicio(request):
    counts = {
        "provincias": TbProvincia.objects.count(), "cantones": TbCanton.objects.count(),
        "estudiantes": TbEstudiantes.objects.count(), "universidades": TbUniversidades.objects.count(),
    }
    recientes = TbEstudiantes.objects.select_related("id_canton").order_by("-fecha_actualizacion_est")[:5]
    return render(request, "principal/inicio.html", {"counts": counts, "recientes": recientes, "active_menu": "inicio"})


def provincia_list(request): return _list(request, "provincia")
def provincia_create(request): return _form(request, "provincia")
def provincia_edit(request, pk): return _form(request, "provincia", pk)
def provincia_detail(request, pk): return _detail(request, "provincia", pk)
def provincia_delete(request, pk): return _delete(request, "provincia", pk)

def canton_list(request): return _list(request, "canton")
def canton_create(request): return _form(request, "canton")
def canton_edit(request, pk): return _form(request, "canton", pk)
def canton_detail(request, pk): return _detail(request, "canton", pk)
def canton_delete(request, pk): return _delete(request, "canton", pk)

def estudiante_list(request): return _list(request, "estudiante")
def estudiante_create(request): return _form(request, "estudiante")
def estudiante_edit(request, pk): return _form(request, "estudiante", pk)
def estudiante_detail(request, pk): return _detail(request, "estudiante", pk)
def estudiante_delete(request, pk): return _delete(request, "estudiante", pk)

def universidad_list(request): return _list(request, "universidad")
def universidad_create(request): return _form(request, "universidad")
def universidad_edit(request, pk): return _form(request, "universidad", pk)
def universidad_detail(request, pk): return _detail(request, "universidad", pk)
def universidad_delete(request, pk): return _delete(request, "universidad", pk)

def procesarActualizacionProvincia(request): return _legacy_update(request, "provincia", "id_provincia")
def procesarActualizacionCanton(request): return _legacy_update(request, "canton", "id_canton")
def procesarActualizacionEstudiante(request): return _legacy_update(request, "estudiante", "id_est")

nuevaProvincia = provincia_create
guardarProvincia = provincia_create
showProvincia = provincia_list
editarProvincia = provincia_edit
eliminarProvincia = provincia_delete
nuevoCanton = canton_create
guardarCanton = canton_create
showCanton = canton_list
editarCanton = canton_edit
eliminarCanton = canton_delete
nuevoEstudiante = estudiante_create
guardarEstudiante = estudiante_create
showEstudiante = estudiante_list
editarEstudiante = estudiante_edit
eliminarEstudiante = estudiante_delete
