from django.core.mail import send_mail

from applications.spam.models import Contact
from shop.celery import app


@app.task
def spam_email():
    for users in Contact.objects.all():
        full_link = f'Привет'
        send_mail(
            'From shop project',
            full_link,
            'sulimanovuran@gmail.com',
            [users.email]
        )


@app.task
def spam_email2(info):
    for users in Contact.objects.all():
        full_link = f'Привет {users.email}, на сайте появился новый продукт: {info}'
        send_mail(
            'From shop project',
            full_link,
            'sulimanovuran@gmail.com',
            [users.email]
        )
