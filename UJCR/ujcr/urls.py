from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from blogs.views import Pdf_view
from main_app.views import index, Search

from django.views.static import serve as mediaserve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls, name="admin-panel"),

    path('', index, name="home"),
    path("", include("blogs.urls")),
    path("", include("main_app.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("il8n/", include("django.conf.urls.i18n")),
    path('search/', Search.as_view(), name="search"),
    path("", include("blogs.urls")),
    path("", include("main_app.urls")),
)
