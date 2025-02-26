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


class BaseViewSet(ModelViewSet):
    OutputSerializer = None
    InputSerializer = None

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            if not self.InputSerializer:
                raise ValidationError(
                    f"{self.__class__.__name__}: InputSerializer is not defined, but is required for {self.action}."
                )
            return self.InputSerializer
        if not self.OutputSerializer:
            raise ValidationError(
                f"{self.__class__.__name__}: OutputSerializer is not defined, but is required for {self.action}."
            )
        return self.OutputSerializer


class BaseAdminViewSet(AdminPermissionMixin, BaseViewSet):
    def perform_create(self, serializer):
        self.check_admin_permissions()
        serializer.save()

    def perform_update(self, serializer):
        self.check_admin_permissions()
        serializer.save()

    def perform_destroy(self, instance):
        self.check_admin_permissions()
        instance.delete()


class SkillTypeViewSet(BaseAdminViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = SkillType.objects.all()
    OutputSerializer = SkillTypeSerializer
    InputSerializer = SkillTypeInputSerializer


class SkillViewSet(BaseAdminViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Skill.objects.all()
    OutputSerializer = SkillSerializer
    InputSerializer = SkillInputSerializer


class ProfessionTypeViewSet(BaseAdminViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ProfessionType.objects.all()
    OutputSerializer = ProfessionTypeSerializer
    InputSerializer = ProfessionTypeInputSerializer


class ProfessionViewSet(BaseAdminViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Profession.objects.all()
    OutputSerializer = ProfessionSerializer
    InputSerializer = ProfessionInputSerializer


class UserSkillViewSet(UserPermissionMixin, ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = UserSkill.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserSKillInputSerializer
        return UserSkillSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        self.check_user_permissions(serializer.instance.user)
        serializer.save()

    def perform_destroy(self, instance):
        self.check_user_permissions(instance.user)
        instance.delete()


class UserProfessionViewSet(UserPermissionMixin, ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Profession.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserProfessionInputSerializer
        return UserProfessionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        self.check_user_permissions(serializer.instance.user)
        serializer.save()

    def perform_destroy(self, instance):
        self.check_user_permissions(instance.user)
        instance.delete()


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
