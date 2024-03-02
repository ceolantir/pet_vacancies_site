from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from company.views import page_not_found, server_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('company.urls')),
    path('', include('users.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

handler404 = page_not_found
handler500 = server_error
