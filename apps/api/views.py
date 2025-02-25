from rest_framework.exceptions import PermissionDenied
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
