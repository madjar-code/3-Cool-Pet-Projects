from celery import shared_task
from contacts.models import Contact
from reports.models import (
    MethodChoices,
    StatusChoices,
    NotificationState,
)
from notifications.models import NotificationTemplate
from reports.models import (
    NotificationState,
    StatusChoices,
    MethodChoices,    
)
from smtplib import SMTPException
from twilio.base.exceptions import TwilioException
from notifications.utils import (
    dev_send_email,
    dev_send_sms,
)


def send_notification_by_method(method: MethodChoices, subject: str,
                                body: str, contact: Contact) -> None:
    if method == MethodChoices.EMAIL_METHOD:
        dev_send_email(subject=subject, body=body, recipient_list=[contact.email])
    elif method == MethodChoices.PHONE_METHOD:
        dev_send_sms(body=body, phone_number=contact.phone)


@shared_task(time_limit=20)
def send_notification(notification_template_id: str,
                      contact_id: str) -> None:
    notification_template = NotificationTemplate.\
                objects.filter(id=notification_template_id).first()
    contact: Contact = Contact.objects.filter(id=contact_id).first()
    notification_state = NotificationState.objects.filter(
        notification_template=notification_template,contact=contact
    ).first()

    if not notification_state:
        if contact.email:
            method = MethodChoices.EMAIL_METHOD
        elif contact.phone:
            method = MethodChoices.PHONE_METHOD

        notification_state = NotificationState.objects.create(
            notification_template=notification_template,
            status=StatusChoices.STATUS_DIRTY,
            contact=contact,
            method=method
        )

    method = notification_state.method

    if notification_state.status == StatusChoices.STATUS_DIRTY:
        subject: str = notification_template.render_title()
        body: str = notification_template.render_text()
        try:
            send_notification_by_method(method, subject, body, contact)
            notification_state.status = StatusChoices.STATUS_READY
        except (SMTPException, TwilioException):
            notification_state.status = StatusChoices.STATUS_FAILED
        notification_state.save()

    # print(f"Задача send_notification выполнена для contact_id: {contact_id}")
