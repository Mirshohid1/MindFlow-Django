from rest_framework.permissions import IsAuthenticatedOrReadOnly

from users.models import SkillType, Skill
from users.serializers import SkillTypeSerializer, SkillTypeInputSerializer, SkillSerializer, SkillInputSerializer

from api.views.base import BaseAdminViewSet


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