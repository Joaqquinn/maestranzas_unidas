from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def crear_profile_al_crear_usuario(sender, instance, created, **kwargs):
    """
    Cada vez que un User se crea, crea también su Profile asociado.
    """
    if created:
        Profile.objects.create(user=instance)