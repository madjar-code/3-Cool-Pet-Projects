from datetime import timedelta
from uuid import UUID
from celery import shared_task, Task
from celery.utils.log import get_task_logger
from smtplib import SMTPException
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
    dev_send_email_wrong,
    dev_send_sms_wrong
)


logger = get_task_logger(__name__)


@shared_task(queue='default_queue')
def periodic_counts(session_id: UUID):
    for i in range(5):
        logger.error(f'\n\n\n{session_id}\n\n\n')
        timedelta(2)


class SendException(Exception):
    """
    Raise SendException when there are
    problems sending notifications
    """


class BaseTaskWithRetry(Task):
    autoretry_for = (SendException,)
    retry_kwargs = {'max_retries': 5,
                    'countdown': 10}
    retry_backoff = False


def send_notification_by_method(method: MethodChoices, subject: str,
                                body: str, contact: Contact) -> None:
    if method == MethodChoices.EMAIL_METHOD:
        dev_send_email(
            subject=subject, body=body, recipient_list=[contact.email])
    elif method == MethodChoices.PHONE_METHOD:
        dev_send_sms(body=body, phone_number=contact.phone)


@shared_task(time_limit=5, base=BaseTaskWithRetry)
def send_notification(session_id: UUID,
                      contact_id: UUID) -> None:
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
    if notification_state.status != StateStatusChoices.STATUS_READY:
        template = notification_session.notification_template
        subject: str = template.render_title()
        body: str = template.render_text()
        try:
            send_notification_by_method(
                notification_state.method, subject, body, contact)
            notification_state.status = StateStatusChoices.STATUS_READY
            notification_state.save()
        except (SMTPException, TwilioException) as e:
            logger.error(f'\n\nFailed to send notification: {str(e)}\n\n')
            notification_state.status = StateStatusChoices.STATUS_FAILED
            notification_state.save()
            current_retry: int = send_notification.request.retries
            max_retries = send_notification.max_retries
            if current_retry < max_retries:
                raise SendException
