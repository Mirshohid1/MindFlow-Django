from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from core.utils import clean_text_for_unique_fields

from datetime import date


def path_to_avatar(instance, filename):
    return f"media/user_{instance.id}/avatar-{filename}"


class CustomUser(AbstractUser):
    CHOICES_ROLE = [
        ('user', 'User'),
        ('admin', 'Admin')
    ]

    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    avatar = models.ImageField(upload_to=path_to_avatar, null=True, blank=True, verbose_name=_("Avatar"))
    bio = models.TextField(null=True, blank=True, verbose_name=_("Bio"))
    role = models.CharField(max_length=10, choices=CHOICES_ROLE, default='user')
    birth_date = models.DateField()

    def get_age(self):
        if not self.birth_date:
            return None
        current_date = date.today()
        age = current_date.year - self.birth_date.year
        if (current_date.month, current_date.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    def clean(self):
        if self.username:
            self.username = clean_text_for_unique_fields(self.username)
        if self.first_name:
            self.first_name = clean_text_for_unique_fields(self.first_name)
        if self.last_name:
            self.last_name = clean_text_for_unique_fields(self.last_name)
        if self.email:
            self.email = clean_text_for_unique_fields(self.email)
        if self.bio:
            self.bio = clean_text_for_unique_fields(self.bio)
        super().clean()

    def save(self, *args, **kwargs):
        super().full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}: {self.role}"


class SkillType(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name=_('Description'))

    def clean(self):
        if self.name:
            self.name = clean_text_for_unique_fields(self.name)
        if self.description:
            self.description = clean_text_for_unique_fields(self.description)

    def save(self, *args, **kwargs):
        super().full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name=_('Description'))
    skill_type = models.ForeignKey(SkillType, on_delete=models.PROTECT, related_name='skills', verbose_name=_("Skill Type"))

    def clean(self):
        if self.name:
            self.name = clean_text_for_unique_fields(self.name)
        if self.description:
            self.description = clean_text_for_unique_fields(self.description)

    def save(self, *args, **kwargs):
        super().full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.skill_type.name}"


class ProfessionType(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name=_('Description'))

    def clean(self):
        if self.name:
            self.name = clean_text_for_unique_fields(self.name)
        if self.description:
            self.description = clean_text_for_unique_fields(self.description)

    def save(self, *args, **kwargs):
        super().full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Profession(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    description = models.TextField(max_length=700, null=True, blank=True, verbose_name=_('Description'))
    profession_type = models.ForeignKey(ProfessionType, on_delete=models.PROTECT, related_name='professions', verbose_name=_("Profession Type"))
    required_skills = models.ManyToManyField(Skill, related_name="professions", verbose_name=_("Required Skills"))

    def clean(self):
        if self.name:
            self.name = clean_text_for_unique_fields(self.name)
        if self.description:
            self.description = clean_text_for_unique_fields(self.description)

    def save(self, *args, **kwargs):
        super().full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.profession_type.name}"


class UserSkill(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_skills', verbose_name=_("User"))
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='user_skills', verbose_name=_("Skill"))
    added_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Added At"))

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user.username}, skill: {self.skill.name}"


class UserProfession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_professions', verbose_name=_("User"))
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, related_name='user_professions', verbose_name=_("Profession"))
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Assigned At"))

    class Meta:
        unique_together = ('user', 'profession')

    def __str__(self):
        return f"{self.user.username}, profession: {self.profession.name}"
