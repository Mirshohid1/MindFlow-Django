from typing import Dict, Any

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    CustomUser, UserSkill, UserProfession,
    SkillType, Skill, ProfessionType, Profession
)


class SkillTypeSerializer(serializers.ModelSerializer):
    pass


class SkillTypeInputSerializer(serializers.ModelSerializer):
    pass


class SkillSerializer(serializers.ModelSerializer):
    pass


class SkillInputSerializer(serializers.ModelSerializer):
    pass


class ProfessionTypeSerializer(serializers.ModelSerializer):
    pass


class ProfessionTypeInputSerializer(serializers.ModelSerializer):
    pass


class ProfessionSerializer(serializers.ModelSerializer):
    pass


class ProfessionInputSerializer(serializers.ModelSerializer):
    pass


class UserSkillSerializer(serializers.ModelSerializer):
    pass


class UserSKillInputSerializer(serializers.ModelSerializer):
    pass


class UserProfessionSerializer(serializers.ModelSerializer):
    pass


class UserProfessionInputSerializer(serializers.ModelSerializer):
    pass


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password_confirm')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            return serializers.ValidationError({'password_confirm': "Passwords don't match!"})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        token['id'] = user.id

        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validated_data(attrs)

        data.update({
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role
        })

        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        try:
            token = RefreshToken(data["refresh"])
            token.blacklist()
        except Exception:
            raise serializers.ValidationError("Invalid token")

        return {"message": "Logout completed"}
