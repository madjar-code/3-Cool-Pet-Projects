from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from users.models import User
from texts.models import TextBlock


class TestTextBlockViews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='test', email='test@test.com', password='test')
        cls.text_block1 = mixer.blend(
            TextBlock, author=cls.user, text=mixer.faker.text())
        cls.text_block2 = mixer.blend(
            TextBlock, author=cls.user, text=mixer.faker.text())
        cls.text_block3 = mixer.blend(
            TextBlock, text=mixer.faker.text())
        cls.text_block4 = mixer.blend(
            TextBlock, text=mixer.faker.text())

    def get_text_block_url(self, hash):
        return reverse('texts:text_block_detail', kwargs={'hash': hash})

    def get_text_blocks_for_user_url(self, username):
        return reverse('texts:text_blocks_for_user', kwargs={'username': username})

    def test_getting_text_block(self):
        url = self.get_text_block_url(self.text_block1.hash)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_text_block_wrong_data(self):
        url = self.get_text_block_url('1' * 20)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_getting_text_blocks_for_user(self):
        url = self.get_text_blocks_for_user_url(self.user.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_text_blocks_for_user_wrong_data(self):
        url = self.get_text_blocks_for_user_url('1' * 20)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)