from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import UserDetails, WishList, User
from django.db import transaction


# @receiver(post_save, sender=User)
# def create_userDetails(sender, instance, created, **kwargs):
#     if created:
#         UserDetails.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def create_wishlist(sender, instance, created, **kwargs):
#     user_details = UserDetails.objects.get(user=instance)
#     if created and user_details:
#         wishlist = WishList.objects.create(userDetails=instance)  
        
        
    #юзер создался создается юзер детейлс создается вишлист в отдельной функции надо чтобы все было пресейв попробуй если не будет получаться то пробуй как хочешь и делай что хочешь
    
# @receiver(post_save, sender=User)
# def create_userDetails_and_wishlist(sender, instance, created, **kwargs):
#     if created:
#         print('aloha')
#         with transaction.atomic():    
#             user_details = UserDetails.objects.create(user=instance)
#             wishlist, wishlist_created = WishList.objects.create(user=user_details)
#             user_details.wishlist = wishlist
#             user_details.save()    
#         print('end')