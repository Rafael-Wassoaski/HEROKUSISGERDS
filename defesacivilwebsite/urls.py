from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ws/', include('ws.urls')),
    path('', include('relatorios.urls')),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('accounts.urls')), # new
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns+= staticfiles_urlpatterns()
