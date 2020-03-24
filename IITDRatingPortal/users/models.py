from django.contrib.auth.models import User
from django.db import models



# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class Rating(models.Model):
    class Meta:
        abstract=True


class UserWarning(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time = models.DateTimeField(default=now,blank=True)
    message = models.CharField(max_length=250)
    # rating_cause = models.ForeignKey(Rating,on_delete=models.CASCADE)

class UserProfile(models.Model):
    respect_points = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_banned = models.BooleanField(default=False)
    ban_days=models.IntegerField(default=0)
    banned_on=models.DateTimeField(default=now,blank=True)
    indefinite_ban=models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

