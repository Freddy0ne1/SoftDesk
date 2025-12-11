from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from authentication.views import UserViewSet
from projects.views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet

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
    # On inclut toutes les URLs générées par le routeur
    path("api/", include(router.urls))

]
