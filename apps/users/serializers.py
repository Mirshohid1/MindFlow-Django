from typing import Dict, Any

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    CustomUser, UserSkill, UserProfession,
    SkillType, Skill, ProfessionType, Profession
)


### --- SKILL SERIALIZERS --- ###

class SkillTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillType
        fields = ('id', 'name', 'description')


class SkillTypeInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillType
        fields = ('name', 'description')


class SkillSerializer(serializers.ModelSerializer):
    skill_type = SkillTypeSerializer()
    class Meta:
        model = Skill
        fields = ('id', 'name', 'description', 'skill_type')


class SkillInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('name', 'description', 'skill_type')


### --- PROFESSION SERIALIZERS --- ###

class ProfessionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionType
        fields = ('id', 'name', 'description')


class ProfessionTypeInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionType
        fields = ('name', 'description')


class ProfessionSerializer(serializers.ModelSerializer):
    profession_type = ProfessionTypeSerializer()
    required_skills = SkillSerializer(many=True)

    class Meta:
        model = Profession
        fields = ('id', 'name', 'description', 'profession_type', 'required_skills')


class ProfessionInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('name', 'description', 'profession_type', 'required_skills')


### --- USER SERIALIZERS --- ###

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role')


### --- USER-SKILL RELATION SERIALIZERS --- ###

class UserSkillSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    skill = SkillSerializer()

    class Meta:
        model = UserSkill
        fields = ('id', 'user', 'skill', 'added_at')


class UserSKillInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = ('skill', )


### --- USER-PROFESSION RELATION SERIALIZERS --- ####

class UserProfessionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    profession = ProfessionSerializer()

    class Meta:
        model = UserProfession
        fields = ('id', 'user', 'profession', 'assigned_at')


class UserProfessionInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfession
        fields = ('profession', )

### --- AUTH SERIALIZERS (REGISTER & LOGIN) --- ###

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
