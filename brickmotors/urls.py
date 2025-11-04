from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # raiz do site aponta direto para as URLs do market
    path("", include(("market.urls", "market"), namespace="market")),

    path("pagamentos/", include(("payments.urls", "payments"), namespace="payments")),
    
    path("conta/", include(("brickmotors.accounts.urls", "accounts"), namespace="accounts")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
