from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class FaceSignature(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	signatures=models.TextField(null=True)
	face=models.TextField(null=True)
	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_user_face_signeture(sender, instance, created, **kwargs):
    if created:
        FaceSignature.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_face_signeture(sender, instance, **kwargs):
	if(instance.facesignature is None):
		FaceSignature.objects.create(user=instance)
	else:
		instance.facesignature.save()


class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='profile',on_delete=models.CASCADE)
	firstname=models.CharField(max_length=100, default='', blank=True)
	lastname=models.CharField(max_length=100, default='', blank=True)
	photo = models.ImageField(null=True, blank=True)
	website = models.URLField(default='', blank=True)
	bio = models.TextField(default='', blank=True)
	phone = models.CharField(max_length=20, blank=True, default='')
	city = models.CharField(max_length=100, default='', blank=True)
	country = models.CharField(max_length=100, default='', blank=True)
	organization = models.CharField(max_length=100, default='', blank=True)

	def __str__(self):
		return self.user.username


@receiver(post_save, sender=User)
def create_update_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)
	instance.profile.save()


