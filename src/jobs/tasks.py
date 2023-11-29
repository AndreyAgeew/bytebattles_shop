from src.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS
from src.jobs.celery import celery
from src.jobs.email_sender import create_order_confirmation_template
import smtplib


@celery.task
def send_order_confirmation_email(email_to, order):
    print(1)
    msg_content = create_order_confirmation_template(email_to, order)

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg_content)
