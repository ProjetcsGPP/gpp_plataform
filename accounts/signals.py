"""
Signals para auto-criação de UserProfile quando um User é criado.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Cria automaticamente um UserProfile quando um User é criado.
    """
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Salva o UserProfile quando o User é salvo.
    Trata o caso onde o profile pode não existir.
    """
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        # Se não existe profile, cria um
        UserProfile.objects.create(user=instance)
