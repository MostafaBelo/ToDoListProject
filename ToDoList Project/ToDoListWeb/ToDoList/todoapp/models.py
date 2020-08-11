from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class data(models.Model):
    task = models.CharField(max_length=100)
    duedate = models.DateField()
    person = models.CharField(max_length=20)
    done = models.BooleanField(default=False)
    task_user = models.IntegerField()

    def __str__(self):
        return self.task

#post_save.connect(create_auth_token, sender=settings.AUTH_USER_MODEL) = @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# they are used to connect the signal(trigger) with the function that runs upon the triggering
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# # custom user manager model
# class MyAccountManager(BaseUserManager):
#
#     # include first_name in paramaters if required
#     def create_user(self, email, username, first_name, password=None):
#         if not email:
#             raise ValueError('User must have an email')
#         if not username:
#             raise ValueError('User must have a username')
#         # if not first_name:
#         #     raise ValueError('User must have a first name')
#
#         user = self.model(
#             email = self.normalize_email(email),
#             username = username,
#         )
#
#         user.set_password(password)
#         user.save(using=self.db)
#         return user
#
#     def create_superuser(self, email, username, password):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             password=password,
#             username=username,
#         )
#
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self.db)
#         return user
#
# # custom user model
# class account(AbstractBaseUser):
#     email = models.EmailField(verbose_name='email', max_length=60, unique=True)
#     username = models.CharField(max_length=30, unique=True)
#     first_name = models.CharField(max_length=30)
#     # required for custom user model
#     date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
#     is_admin = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     # required for custom user model
#     USERNAME_FIELD = 'email'
#     # include first_name if required
#     REQUIRED_FIELDS = ['username',]
#
#     objects = MyAccountManager()
#
#     def __str__(self):
#         return self.email + ': ' + self.username
#
#     # required functions
#     def has_perm(self, per, obj=None):
#         return self.is_admin
#
#     def has_module_perms(self, app_label):
#         return True
#     # required functions
