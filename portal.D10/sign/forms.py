from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


class BasicSignupForm(SignupForm):
    
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)

        # send_mail(
        # subject='Welcome to News Portal! Thanks for registration.',
        # message='You have been registered at News Portal.',
        # from_email=None,
        # recipient_list=[user.email, ],
        # # fail_silently=True
        # ) #отправка письма при регистрации

        html_content = render_to_string('email_confirmation_signup_message.html')
        signup_message = EmailMultiAlternatives(
            subject='Welcome to News Portal! Thanks for registration.',
            body='You have been registered at News Portal.',
            from_email=None,
            to=[user.email, ]
        )
        signup_message.attach_alternative(html_content, 'text/html')
        signup_message.send()  # отправка писем при регистрации

        return user