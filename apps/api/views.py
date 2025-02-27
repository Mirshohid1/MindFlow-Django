from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework import status
from users.models import (
    CustomUser, UserSkill, UserProfession,
    SkillType, Skill, ProfessionType, Profession
)
from users.serializers import (
    SkillTypeSerializer, SkillTypeInputSerializer,
    SkillSerializer, SkillInputSerializer,
    ProfessionTypeSerializer, ProfessionTypeInputSerializer,
    ProfessionSerializer, ProfessionInputSerializer,
    UserSkillSerializer, UserSKillInputSerializer,
    UserProfessionSerializer, UserProfessionInputSerializer,
    RegisterSerializer, LoginSerializer
)
from api.mixins import AdminPermissionMixin, UserPermissionMixin


class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            return Response({
                "token": data['token'],
                "user": {
                    "id": data['id'],
                    "username": data['username'],
                    "email": data['email'],
                    "role": data['role']
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(TokenBlacklistView):
    permission_classes = [IsAuthenticated]
    serializer_class = TokenBlacklistSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
