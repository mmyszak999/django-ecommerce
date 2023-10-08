from uuid import UUID

from rest_framework import permissions, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin
)

from src.apps.users.models import UserAddress, UserProfile
from src.apps.users.serializers import (
    RegistrationInputSerializer,
    RegistrationOutputSerializer,
    UserOutputSerializer,
    UpdateUserSerializer,
    UserDetailOutputSerializer
)
from src.apps.users.services import UserProfileCreateService, UserUpdateService


class UserRegisterAPIView(GenericViewSet, CreateModelMixin):
    serializer_class = RegistrationOutputSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request: Request) -> Response:
        service = UserProfileCreateService()
        serializer = RegistrationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_profile = service.register_user(request_data=serializer.validated_data)
        return Response(
            self.get_serializer(user_profile).data,
            status=status.HTTP_201_CREATED
        )


class UserProfileListAPIView(GenericViewSet, ListModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserOutputSerializer
    
    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(user=user)


class UserProfileDetailAPIView(GenericViewSet, RetrieveModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserDetailOutputSerializer
    
    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(user=user)

    def update(self, request: Request, pk: UUID) -> Response:
        service = UserUpdateService()
        instance = self.get_object()
        serializer = UpdateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_userprofile = service.update_user(
            request_data=serializer.validated_data, instance=instance
        )
        return Response(
            self.get_serializer(updated_userprofile).data, status=status.HTTP_200_OK
        )
    