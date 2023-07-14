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
    SessionStatusChoices,
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
        # session_filter = NotificationSession.objects.filter(id=session_id)
        try:
            # session_filter.update(during_counter=F('during_counter') + 1)
            send_notification_by_method(
                notification_state.method, subject, body, contact)
            notification_state.status = StateStatusChoices.STATUS_READY
            notification_state.save()
            # session_filter.update(success_counter=F('success_counter') + 1)
        except (SMTPException, TwilioException):
            notification_state.status = StateStatusChoices.STATUS_FAILED
            notification_state.save()
            # session_filter.update(success_counter=F('failed_counter') + 1)
        finally:
            pass
            # session_filter.update(during_counter=F('during_counter') - 1)
            # counters = session_filter.values('success_counter', 'failed_counter', 'all_counter').first()
            # success_counter = int(counters['success_counter'])
            # failed_counter = int(counters['failed_counter'])
            # all_counter = int(counters['all_counter'])

            # if all_counter > 0 and success_counter + failed_counter == all_counter:
            #     session_filter.update(status=SessionStatusChoices.STATUS_READY)
            # elif all_counter > 0:
            #     session_filter.update(status=SessionStatusChoices.STATUS_DURING)
