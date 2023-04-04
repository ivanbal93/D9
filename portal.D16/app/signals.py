from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, send_mail
from .models import Post, Category, User
from django.template.loader import render_to_string
from datetime import datetime

@receiver(post_save, sender=Post)  # отправка новых постов подписчикам категории
def notify_subscribers(sender, instance, created, **kwargs):
    if instance.category.exists():
        category_for_subscribe = Category.objects.filter(id=instance.category)
        html_content = render_to_string('new_post_email.html')
        link = f'http://127.0.0.1:8000/news/{instance.id}'
        for subscriber in category_for_subscribe.values('subscribers'):
            message = EmailMultiAlternatives(
                subject='New post in your favorite category!',
                body=f'{instance.post_text[:50]}.../n{link}',
                from_email=None,
                to=[User.objects.get(id=subscriber['subscribers']).email, ]
            )
            message.attach_alternative(html_content, 'text/html')
            message.send()