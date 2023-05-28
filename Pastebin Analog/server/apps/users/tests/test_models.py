from django.test import TestCase
from mixer.backend.django import mixer
from users.models import User


class TestUserModel(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            'user','user@user.com', '12345')
    
    def test_creation(self) -> None:
        self.assertEqual(str(self.user), 'user')
        self.assertEqual(self.user.description, None)
