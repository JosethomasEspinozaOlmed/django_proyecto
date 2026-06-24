from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "",
        include("apps.propiedades.urls"),
    ),
    path(
        "usuarios/",
        include("apps.usuarios.urls"),
    ),
    path(
        "contactos/",
        include("apps.contactos.urls"),
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
