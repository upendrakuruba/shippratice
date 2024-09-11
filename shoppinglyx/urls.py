from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name='home'),
    path('app/', include('app.urls')),
    path('', include('category.urls')),
    path('store/', include('store.urls')),
    path('', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



handler404 = "accounts.views.my_custom_page_not_found_view"
handler500 = "accounts.views.my_custom_server_error_view"