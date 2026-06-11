from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_nested import routers
from . import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")

users_router = routers.NestedDefaultRouter(router, "users", lookup="user")
users_router.register(r"tplace", views.TplaceViewSet, basename="tplace")
users_router.register(r"nyancoins", views.NyancoinsViewSet, basename="nyancoins")
users_router.register(r"colors", views.ColorsViewSet, basename="colors")
users_router.register(r"pixels", views.PixelsViewSet, basename="pixels")
users_router.register(r"max-pixels", views.MaxPixelsViewSet, basename="max-pixels")

urlpatterns = [
    path("", views.index, name="index"),
    path("api/", include(router.urls)),
    path("api/", include(users_router.urls)),
    path("api/login", views.LoginView.as_view()),
    path("api-auth/signup", views.signup),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("accounts/profile/", views.profile, name="profile"),
    path("accounts/signup", views.signup, name="signup"),
    path("accounts/modify", views.account_modify, name="account_modify"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
