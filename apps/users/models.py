from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


def path_to_avatar(instance, filename):
    return f"media/user_{instance.id}/avatar-{filename}"


class CustomUser(AbstractUser):
    CHOICES_ROLE = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('developer', 'Developer')
    ]

    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    avatar = models.ImageField(upload_to=path_to_avatar, null=True, blank=True, verbose_name=_("Avatar"))
    bio = models.TextField(null=True, blank=True, verbose_name=_("Bio"))
    role = models.CharField(max_length=10, choices=CHOICES_ROLE, default='user')
    birth_date = models.DateField()


class SkillType(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name=_('Description'))


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name=_('Description'))
    skill_type = models.ForeignKey(SkillType, on_delete=models.PROTECT, related_name='skills', verbose_name=_("Skill Type"))


class Profession(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    required_skills = models.ManyToManyField(Skill, related_name="professions", verbose_name=_("Required Skills"))


class UserSkill(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_skills', verbose_name=_("User"))
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='user_skills', verbose_name=_("Skill"))
    added_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Added At"))

    class Meta:
        unique_together = ('user', 'skill')


class UserProfession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_professions', verbose_name=_("User"))
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, related_name='user_professions', verbose_name=_("Profession"))
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Assigned At"))

    class Meta:
        unique_together = ('user', 'profession')