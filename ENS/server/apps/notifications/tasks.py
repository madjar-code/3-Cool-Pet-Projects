from django.db import transaction
from celery import shared_task
from smtplib import SMTPException
from django.db.models import F
from twilio.base.exceptions import\
    TwilioException
from contacts.models import (
    Contact,
)
from reports.models import (
    MethodChoices,
    StateStatusChoices,
    NotificationState,
    NotificationSession,
)
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
def send_notification(session_id: str,
                      contact_id: str) -> None:
    notification_session = NotificationSession.objects.filter(id=session_id).first()
    contact: Contact = Contact.objects.filter(id=contact_id).first()
    
    if not notification_session or not contact:
        return

    notification_state, _ = NotificationState.objects.get_or_create(
        notification_session=notification_session,
        contact=contact,
        defaults={
            'status': StateStatusChoices.STATUS_DIRTY,
            'method': MethodChoices.EMAIL_METHOD\
                if contact.email else MethodChoices.PHONE_METHOD
        }
    )
    if notification_state.status == StateStatusChoices.STATUS_DIRTY:
        template = notification_session.notification_template
        subject: str = template.render_title()
        body: str = template.render_text()
        try:
            NotificationSession.objects.filter(id=session_id).\
                    update(during_counter=F('during_counter') + 1)
            send_notification_by_method(
                notification_state.method, subject, body, contact)
            notification_state.status = StateStatusChoices.STATUS_READY
            notification_state.save()
            NotificationSession.objects.filter(id=session_id).\
                update(success_counter=F('success_counter') + 1)
        except (SMTPException, TwilioException):
            notification_state.status = StateStatusChoices.STATUS_FAILED
            notification_state.save()
            NotificationSession.objects.filter(id=session_id).\
                update(success_counter=F('failed_counter') + 1)
        finally:
            NotificationSession.objects.filter(id=session_id).\
                update(during_counter=F('during_counter') - 1)