from rest_framework import permissions, generics, status
from rest_framework.response import Response

from src.apps.users.models import UserAddress, UserProfile
from src.apps.users.serializers import (
    RegistrationInputSerializer,
    RegistrationOutputSerializer,
    UserProfileListOutputSerializer
)
from src.apps.users.services import UserProfileCreateService


class UserRegisterAPIView(generics.GenericAPIView):
    serializer_class = RegistrationOutputSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        service = UserProfileCreateService()
        serializer = RegistrationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_profile = service.register_user(request_data=serializer.validated_data)
        return Response(
            self.get_serializer(user_profile).data,
            status=status.HTTP_201_CREATED
        )


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListOutputSerializer