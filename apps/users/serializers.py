from typing import Dict, Any

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
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
    skill_type = SkillTypeSerializer(read_only=True)
    class Meta:
        model = Skill
        fields = ('id', 'name', 'description', 'skill_type')


class SkillInputSerializer(serializers.ModelSerializer):
    skill_type = serializers.PrimaryKeyRelatedField(
        queryset=SkillType.objects.all()
    )

    class Meta:
        model = Skill
        fields = ('name', 'description', 'skill_type')

    def to_internal_value(self, data):
        skill_type_data = data.get('skill_type')

        if isinstance(skill_type_data, dict):
            try:
                skill_type = SkillType.objects.get(**skill_type_data)
            except SkillType.DoesNotExist:
                raise serializers.ValidationError(
                    {"skill_type": "Skill type not found, provide a valid ID."}
                )
            data['skill_type'] = skill_type.id

        return super().to_internal_value(data)


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
    profession_type = ProfessionTypeSerializer(read_only=True)
    required_skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Profession
        fields = ('id', 'name', 'description', 'profession_type', 'required_skills')


class ProfessionInputSerializer(serializers.ModelSerializer):
    profession_type = PrimaryKeyRelatedField(
        queryset=ProfessionType.objects.all()
    )
    required_skills = PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True
    )

    class Meta:
        model = Profession
        fields = ('name', 'description', 'profession_type', 'required_skills')

    def to_internal_value(self, data):
        profession_type_data = data.get('profession_type')
        required_skills_data = data.get('required_skills', [])

        if required_skills_data and isinstance(required_skills_data, list):
            skill_ids = []
            for skill in required_skills_data:
                if isinstance(skill, dict):  # Nested object
                    try:
                        skill_obj = Skill.objects.get(**skill)
                    except Skill.DoesNotExist:
                        raise serializers.ValidationError(
                            {"required_skills": "Some skills were not found, provide valid IDs."}
                        )
                    skill_ids.append(skill_obj.id)
                else:  # ID (the usual case)
                    skill_ids.append(skill)

            data['required_skills'] = skill_ids

        if isinstance(profession_type_data, dict):
            try:
                profession_type = ProfessionType.objects.get(**profession_type_data)
            except ProfessionType.DoesNotExist:
                raise serializers.ValidationError(
                    {"profession_type": "Profession type not found, provide a valid ID."}
                )
            data['profession_type'] = profession_type.id

        return super().to_internal_value(data)


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
            raise serializers.ValidationError({'password_confirm': "Passwords don't match!"})
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
        data = super().validate(attrs)

        data.update({
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role
        })

        return data
