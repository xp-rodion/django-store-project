from datetime import timedelta
from uuid import uuid4

from celery import shared_task
from django.utils.timezone import now

from users.models import EmailVerification, User


@shared_task
def send_email_verification(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=24)
    code = uuid4()
    record = EmailVerification.objects.create(code=code, user=user, expiration=expiration)
    record.send_verification_email()