from rest_framework.permissions import IsAuthenticatedOrReadOnly

from users.models import UserSkill, UserProfession
from users.serializers import (
    UserSkillSerializer, UserSKillInputSerializer, UserProfessionSerializer, UserProfessionInputSerializer
)

from api.views.base import BaseUserViewSet


class UserSkillViewSet(BaseUserViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = UserSkill.objects.all()
    OutputSerializer = UserSkillSerializer
    InputSerializer = UserSKillInputSerializer


class UserProfessionViewSet(BaseUserViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = UserProfession.objects.all()
    OutputSerializer = UserProfessionSerializer
    InputSerializer = UserProfessionInputSerializer
