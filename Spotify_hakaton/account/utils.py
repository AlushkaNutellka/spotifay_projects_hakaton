from django.core.mail import send_mail


def send_activation_code(email, activation_code):
    message = f'Congratulations! Вы зарегистрировались на нашем сайте. Активируйте аккаунт отправив нам акивационный код: {activation_code}'

    send_mail('Активация аккаунта',
                message,
                'jiulwinchester@gmail.com',
                [email]
    )