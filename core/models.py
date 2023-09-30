from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def profile(self):
        try:
            return self.profile
        except Profile.DoesNotExist:
            return None

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000, default=None)
    bio = models.CharField(max_length=100)
    image = models.ImageField(upload_to="user_images", default="default.jpg")

    def __str__(self):
        return self.full_name if self.full_name else self.user.username

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

class Message(models.Model):
    body = models.TextField()
    msg_sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_sender")
    msg_receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_receiver")

    def __str__(self):
        return self.body