from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from users.models import User
from texts.models import TextBlock


class TestTextBlockViews(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='test')
        self.text_block1: TextBlock = mixer.blend(
            TextBlock, author=self.user, text=mixer.faker.text())
        self.text_block2: TextBlock = mixer.blend(
            TextBlock, author=self.user, text=mixer.faker.text())
        self.text_block3: TextBlock = mixer.blend(
            TextBlock, text=mixer.faker.text())
        self.text_block4: TextBlock = mixer.blend(
            TextBlock, text=mixer.faker.text())

    def test_getting_text_block(self) -> None:
        """
        Get one text block by hash
        """
        hash: str = self.text_block1.hash
        print(hash)
        response: Response = self.client.get(f'/api/v1/text-blocks/{hash}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_text_block_wrong_data(self) -> None:
        """
        Get one text block with wrong data
        """
        random_hash = '1' * 20
        response: Response = self.client.get(f'/api/v1/text-blocks/{random_hash}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_getting_text_block_to_user(self) -> None:
        """
        Get text blocks to user by username
        """
        username: str = self.user.username
        response: Response = self.client.get(f'/api/v1/text-blocks/user-{username}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_text_block_to_user_wrong_data(self) -> None:
        """
        Get text blocks to user with wrong username
        """
        random_username = '1' * 20
        response: Response = self.client.get(f'/api/v1/text-blocks/user-{random_username}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
