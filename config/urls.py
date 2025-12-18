from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from authentication.views import UserViewSet
from projects.views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# Création du routeur
router = routers.DefaultRouter()

# Route pour l'app authentication
router.register("users", UserViewSet, basename="user")

# Routes pour l'app projects
router.register("projects", ProjectViewSet, basename="project")
router.register("contributors", ContributorViewSet, basename="contributor")
router.register("issues", IssueViewSet, basename="issue")
router.register("comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("admin/", admin.site.urls),

    # URL pour récupérer le token (Login)
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),

    # URL pour rafraîchir le token
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # On inclut toutes les URLs générées par le routeur
    path("api/", include(router.urls))
]
