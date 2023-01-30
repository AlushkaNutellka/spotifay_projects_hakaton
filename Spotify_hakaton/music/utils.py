from django.core.mail import send_mail


def send_activation_code(email, activation_code):
    message = 'Congratulations! Вы активировали VIP'

    send_mail('Активация аккаунта',
                message,
                'jiulwinchester@gmail.com',
                [email]
    )