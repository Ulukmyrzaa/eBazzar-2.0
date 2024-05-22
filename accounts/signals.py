from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User, WishList


# @receiver(post_save, sender=User)
# def create_wishlist(sender, instance, created, **kwargs):
#     if created:
#         WishList.objects.create(user=instance)   