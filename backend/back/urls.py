from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from . import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")

urlpatterns = [
    path("", views.index, name="index"),
    path("api/", include(router.urls)),
    path("api/users/<str:user>/tplace/", views.TplaceView.as_view()),
    path("api/users/<str:user>/nyancoins/", views.NyancoinsView.as_view()),
    path("api/users/<str:user>/colors/", views.ColorsView.as_view()),
    path("api/users/<str:user>/pixels/", views.UserPixelsView.as_view()),
    path("api/users/<str:user>/max-pixels/", views.MaxPixelsView.as_view()),
    path("api/tplace/pixels/", views.PixelPlaceView.as_view()),
    path("api-auth/signup", views.signup),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("accounts/profile/", views.profile, name="profile"),
    path("accounts/signup", views.signup, name="signup"),
    path("accounts/modify", views.account_modify, name="account_modify"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
