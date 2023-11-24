from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Author

@receiver(post_save, sender=User)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance, name_author=instance.username)

@receiver(post_save, sender=User)
def save_author(sender, instance, **kwargs):
    instance.author.save()

