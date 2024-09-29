from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from main.views import Home_Page,Graph_Page
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Home_Page, name='home'),
    path("graph/", Graph_Page, name='graph'),
]


# after comment or remove these
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)