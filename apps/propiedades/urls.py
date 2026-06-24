from django.urls import path

from .views import (
    api_ciudades,
    cambiar_estado_propiedad,
    crear_propiedad,
    detalle_propiedad,
    editar_propiedad,
    eliminar_propiedad,
    inicio,
    mis_publicaciones,
)


urlpatterns = [
    path(
        "",
        inicio,
        name="inicio",
    ),
    path(
        "propiedad/<int:pk>/",
        detalle_propiedad,
        name="detalle_propiedad",
    ),
    path(
        "publicar/",
        crear_propiedad,
        name="crear_propiedad",
    ),
    path(
        "mis-publicaciones/",
        mis_publicaciones,
        name="mis_publicaciones",
    ),
    path(
        "propiedad/<int:pk>/editar/",
        editar_propiedad,
        name="editar_propiedad",
    ),
    path(
        "propiedad/<int:pk>/estado/",
        cambiar_estado_propiedad,
        name="cambiar_estado_propiedad",
    ),
    path(
        "propiedad/<int:pk>/eliminar/",
        eliminar_propiedad,
        name="eliminar_propiedad",
    ),
    path(
        "api/ciudades/",
        api_ciudades,
        name="api_ciudades",
    ),
]
