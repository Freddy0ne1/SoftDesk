from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from authentication.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]