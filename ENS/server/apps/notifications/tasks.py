from celery import shared_task
from contacts.models import Contact
from reports.models import (
    MethodChoices,
    StatusChoices,
    NotificationState,
)
from notifications.models import NotificationTemplate
from notifications.utils import (
    dev_send_email,
)



# @shared_task(bind=True)
# def send_notification(self, notification_template_id: str,
#                       contact_id: str) -> None:
#     notification_template = NotificationTemplate.\
#         objects.filter(id=notification_template_id).first()
#     contact: Contact = Contact.objects.filter(id=contact_id).first()
#     notification_state = NotificationState.objects.create(
#         notification_template=notification_template,
#         contact=contact,
#         status=StatusChoices.STATUS_DIRTY,
#         method=MethodChoices.EMAIL_METHOD,
#     )
#     subject: str = notification_template.render_title()
#     body: str = notification_template.render_text()
#     contact_list: str = [contact.email]
#     try:
#         dev_send_email(subject, body, contact_list)
#         notification_state.status = StatusChoices.STATUS_READY
#     except Exception as e:
#         notification_state.status = StatusChoices.STATUS_FAILED
#     notification_state.save()
