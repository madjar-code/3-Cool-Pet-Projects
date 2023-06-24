from django.contrib.auth.tokens import\
    PasswordResetTokenGenerator
from django.utils.crypto import salted_hmac
from django.utils.http import int_to_base36
from notifications.models import NotificationTemplate


class NotificationTokenGenerator(PasswordResetTokenGenerator):
    key_salt = "notification.tokens.NotificationTokenGenerator"

    def make_token(self, notification_template:
                    NotificationTemplate, timestamp: float) -> str:
        notification_template_id = int_to_base36(int(notification_template.id.hex, 16))

        value = f'{notification_template_id}-{timestamp}'
        hash_value = salted_hmac(self.key_salt, value).hexdigest()[::2]

        return f'{notification_template_id}-{timestamp}-{hash_value}'
