from django.contrib.auth.models import User
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from .serializers import RegisterSerializer


class RegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)



