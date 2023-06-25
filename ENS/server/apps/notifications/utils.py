from time import sleep
from typing import List
from smtplib import SMTPException
from django.contrib.auth.tokens import\
    PasswordResetTokenGenerator
from django.utils.crypto import salted_hmac
from django.utils.http import int_to_base36
from django.core.mail import send_mail
from notifications.models import NotificationTemplate


class NotificationTokenGenerator(PasswordResetTokenGenerator):
    key_salt = "notification.tokens.NotificationTokenGenerator"

    def make_token(self, notification_template:
                    NotificationTemplate, timestamp: float) -> str:
        notification_template_id = int_to_base36(int(notification_template.id.hex, 16))

        value = f'{notification_template_id}-{timestamp}'
        hash_value = salted_hmac(self.key_salt, value).hexdigest()[::2]

        return f'{notification_template_id}-{timestamp}-{hash_value}'


def dev_send_email(subject: str, body: str,
                   recipient_list: List[str]) -> None:
    sleep(2)
    send_mail(
        subject, body, 'admin@admin.com',
        recipient_list, fail_silently=False)


def dev_send_email_wrong(subject: str, body: str,
                         recipient_list: List[str]) -> None:
    sleep(2)
    raise SMTPException
