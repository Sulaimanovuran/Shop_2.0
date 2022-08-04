from django.core.mail import send_mail

from shop.celery import app


@app.task
def send_order_email(info, email):
    send_mail(
        'From shop project',
        f'Привет спасибо тебе за заказ.\nМы с тобой свяжемся.\n{info}',
        'sulimanovuran@gmail.com',
        [email]
    )