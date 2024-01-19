from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import UserDetails, WishList


@receiver(post_save, sender=UserDetails)
def create_wishlist(sender, instance, created, **kwargs):
    if created:
        WishList.objects.create(userDetails=instance)   