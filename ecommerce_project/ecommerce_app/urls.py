from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from orders.views import stripe_webhook_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('orders/', include('orders.urls'), name='orders'),
    path("__debug__/", include("debug_toolbar.urls")),
    path('webhooks/stripe/', stripe_webhook_view, name='stripe_webhook'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)

