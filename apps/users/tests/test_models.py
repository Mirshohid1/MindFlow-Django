import pytest
from datetime import date

from users.models import (
    CustomUser, SkillType, Skill,
    ProfessionType, Profession,
    UserSkill, UserProfession,
)


@pytest.mark.django_db
def test_custom_user_clean_and_save():
    user = CustomUser.objects.create(
        username = "L0N3r",
        password = '1234',
        email = "loNer@ExAmple.com",
        first_name = " MiRsHoxId",
        last_name = "    MiRShOXiDoV  ",
    )
    assert (
            user.username == 'l0n3r' and user.email == 'loner@example.com' and
            user.first_name == 'mirshoxid' and user.last_name == 'mirshoxidov'
    )

@pytest.mark.django_db
def test_skill_type_clean_and_save():
    skill_type = SkillType.objects.create(
        name="   LaNGuaGE    PrOgRAmmINg  ",
        description="""
        A        PRoGrAMmIng   LaNGUaGE iS     A           SET         oF       iNsTRuCtIonS          aNd        rULEs         THAT       ENaBlE      the creation and
        management of programs, computers, and other devices. It allows developers to write,
        test, and debug code that performs various tasks and solves problems.
        """
    )
    assert skill_type.name == 'language programming' and " ".join(skill_type.description.split()).lower() == "a programming language is a set of instructions and rules that enable the creation and management of programs, computers, and other devices. it allows developers to write, test, and debug code that performs various tasks and solves problems."

