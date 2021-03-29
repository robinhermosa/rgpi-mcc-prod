from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=100, blank=True)
    contact_no = models.TextField(max_length=20, blank=True)
    site = models.CharField(max_length=20,choices=ASSIGNED_SITE, default="-------------")
    department = models.CharField(max_length=20,choices=DEPARTMENT, default="-------------")
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()