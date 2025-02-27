from rest_framework.permissions import IsAuthenticatedOrReadOnly

from users.models import ProfessionType, Profession
from users.serializers import (
    ProfessionTypeSerializer, ProfessionTypeInputSerializer,
    ProfessionSerializer, ProfessionInputSerializer
)

from api.views.base import BaseAdminViewSet


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
