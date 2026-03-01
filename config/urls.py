from django.contrib import admin
from django.urls import path
from store.views import product_list, product_configure, report_view, clear_cart
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_list, name='product_list'),
    path('configure/<int:product_id>/', product_configure, name='product_configure'),
    path('report/', report_view, name='report_view'),
    path('clear-cart/', clear_cart, name='clear_cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
