from rest_framework import permissions, generics, status
from rest_framework.response import Response

from src.apps.accounts.models import UserAddress, UserProfile
from src.apps.accounts.serializers import (
    RegistrationInputSerializer,
    UserAddressOutputSerializer,
    UserProfileListOutputSerializer,
    UserProfileDetailOutputSerializer,
    RegistrationOutputSerializer,
    UserProfileUpdateInputSerializer,
)
from src.apps.users.services import UserProfileCreateService


class UserRegisterAPIView(generics.GenericAPIView):
    serializer_class = RegistrationOutputSerializer
    permission_classes = [permissions.AllowAny]
    service_class = UserProfileCreateService

    def post(self, request):
        serializer = RegistrationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_profile = self.service_class.register_user(data=serializer.validated_data)
        return Response(
            self.get_serializer(user_profile).data,
            status=status.HTTP_201_CREATED
        )