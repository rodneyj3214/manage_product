from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import (
    UserExtraSerializer,
    UserLoginSerializer,
    UserModelSerializer,
    UserSignupSerializer,
)

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserExtraSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_permissions(self):
        """Allow access for any user in login method"""
        if self.action in ["login"]:
            permissions = [AllowAny]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    @action(detail=False)
    def me(self, request):
        """Show the data of the user token authentication"""
        serializer = UserExtraSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["post"], serializer_class=UserSignupSerializer)
    def signup(self, request):
        """Create new users for admin system"""
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], serializer_class=UserLoginSerializer)
    def login(self, request):
        """LogIn For user, On success return User's info and token"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {"user": UserModelSerializer(user).data, "token": token}
        return Response(data, status=status.HTTP_201_CREATED)
