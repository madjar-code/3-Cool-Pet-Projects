from time import sleep
from typing import List
from smtplib import SMTPException
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from django.conf import settings
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


def dev_send_sms(body: str, phone_number: str,
                 subject: str = None) -> None:
    sleep(2)
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER
    result_string =\
        f'SMS from: {twilio_phone_number}\n'\
        f'To: {phone_number}\n'\
        f'Message Body: {body}\n'
    print(result_string)


def dev_send_sms_wrong(body: str, phone_number: str,
                       subject: str = None) -> None:
    sleep(2)
    raise TwilioException


def send_sms(body: str, phone_number: str,
                 subject: str = None) -> None:
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    client.messages.create(
        body=body, from_=twilio_phone_number, to=phone_number)
