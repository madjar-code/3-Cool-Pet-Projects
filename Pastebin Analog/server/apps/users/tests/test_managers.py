from django.test import TestCase
from users.models import User


class TestUserManager(TestCase):
    def test_user_creation(self) -> None:
        user = User.objects.create_user(
            username='jdoe', email='jdoe@jdoe.com',
            password='password',
        )
        self.assertTrue(isinstance(user, User))

    def test_superuser_creation(self) -> None:
        superuser = User.objects.create_superuser(
            username='jdoe', email='jdoe@jdoe.com',
            password='password',
        )
        self.assertTrue(isinstance(superuser, User))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
