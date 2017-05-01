from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

import base64


# class ServerKeychain(models.Model):
#     private_key = models.OneToOneField(AsymmetricKey, on_delete=models.CASCADE, editable=False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    company = models.NullBooleanField()
    blockedAccess = models.NullBooleanField()

#instantiate keychain_size to 1
#instantiate active to true
#instantiate keychain before key
class ServerKeychain(models.Model):
    active = models.NullBooleanField()
    keychain_size = models.IntegerField()

#intantiate key with name "Primary" and keychain as the one above
#import Crypto.PublicKey.RSA, use it to generate a key with key = RSA.generate(2048)
#finish up by doing privatekey = key.exportKey() to store the private key with
# key.set_key(privatekey)

class ServerKey(models.Model):
    name = models.CharField(max_length=500)
    keychain = models.ForeignKey(ServerKeychain, on_delete=models.CASCADE)
    _key = models.TextField(
            db_column='key',
            blank=True)

    def set_key(self, key):
        self._key = base64.encodebytes(key)

    def get_key(self):
        return base64.decodebytes(self._key.encode())

    key = property(get_key, set_key)

class PrivateKey(models.Model):
    name = models.CharField(max_length=20, blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    _key = models.TextField(
            db_column='key',
            blank=True)

    def set_key(self, key):
        self._key = base64.encodebytes(key)

    def get_key(self):
        return base64.decodebytes(self._key.encode())

    key = property(get_key, set_key)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()

class GroupProfile(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

