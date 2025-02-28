from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

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


class ConfirmEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        confirmation_code = request.data.get("confirmation_code")

        if not confirmation_code:
            return Response({"detail": "The confirmation code is required."}, status=status.HTTP_400_BAD_REQUEST)

        if user.confirmation_code != confirmation_code:
            return Response({"detail": "Invalid confirmation code."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_email_verified = True
        user.confirmation_code = None  # Удаляем код после подтверждения
        user.save()

        return Response({"detail": "Email has been successfully confirmed!"}, status=status.HTTP_200_OK)
