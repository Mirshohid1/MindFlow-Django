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
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ProfessionType.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProfessionTypeInputSerializer
        return ProfessionTypeSerializer

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


class ProfessionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Profession.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProfessionInputSerializer
        return ProfessionSerializer

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


class UserSkillViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = UserSkill.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserSKillInputSerializer
        return UserSkillSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.user:
            raise PermissionDenied("You can't update this object")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise PermissionDenied("You can't destroy this object")
        instance.delete()


class UserProfessionViewSet(ModelViewSet):
    pass


class RegisterView(CreateAPIView):
    pass


class LoginView(TokenObtainPairView):
    pass


class LogoutView(TokenBlacklistView):
    pass