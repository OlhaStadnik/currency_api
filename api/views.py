from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserBalance
from .serializers import RegisterSerializer, UserBalanceSerializer


class RegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


class BalanceView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserBalanceSerializer

    def list(self, request):
        user_balance = get_object_or_404(UserBalance, user=request.user)
        serializer = self.get_serializer(user_balance)
        return Response(serializer.data)
