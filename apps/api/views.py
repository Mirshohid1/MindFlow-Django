from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
    RegisterSerializer, LoginSerializer, LogoutSerializer
)


class SkillTypeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = SkillType.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SkillTypeInputSerializer
        return SkillTypeSerializer

    def perform_create(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied("You do not have the rights to perform this action.")
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied("You do not have the rights to perform this action.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != 'admin':
            raise PermissionDenied("You do not have the rights to perform this action.")
        instance.delete()


class SkillViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Skill.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SkillInputSerializer
        return SkillSerializer

    def perform_create(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied("You do not have the rights to perform this action.")
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied("You do not have the rights to perform this action.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != 'admin':
            raise PermissionDenied("You do not have the rights to perform this action.")
        instance.delete()


class ProfessionTypeViewSet(ModelViewSet):
    pass


class ProfessionViewSet(ModelViewSet):
    pass


class UserSkillViewSet(ModelViewSet):
    pass


class UserProfessionViewSet(ModelViewSet):
    pass


class RegisterView(CreateAPIView):
    pass


class LoginView(TokenObtainPairView):
    pass


class LogoutView(TokenBlacklistView):
    pass