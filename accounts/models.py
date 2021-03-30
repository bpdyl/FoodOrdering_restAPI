from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.

# class accountSchema(models.Model):
#     role_user = "USER"
#     role_seller = "SELLER"
#     role_admin = "ADMIN"
#     email = models.CharField(max_length = 50, blank = True, null = True)
#     password = models.CharField(max_length = 50,)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.user_name


def userprofile_reciever(sender, instance ,created, *args , **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)

post_save.connect(userprofile_reciever, sender = settings.AUTH_USER_MODEL)

# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
#     username = models.CharField(blank=False, max_length=50)
#     first_name = models.CharField(blank=False, max_length=50)
#     last_name = models.CharField(blank = False, max_length=50)
#     profile_image = models.ImageField(upload_to='images', blank=False)
#     contact_no = models.PositiveIntegerField()
#     email = models.EmailField()
#     # x = models.DecimalField(max_digits=9, decimal_places=6,default=0.0)
#     # y = models.DecimalField(max_digits=9, decimal_places=6,default=0.0)

#     def __str__(self):
#         return self.username

# def post_save_profile_create(sender, instance, created, *args, **kwargs):
#     if created:
#         Profile.objects.get_or_create(user = instance)
# post_save.connect(post_save_profile_create, sender = settings.AUTH_USER_MODEL)        

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank = True)
    contact_no = models.PositiveIntegerField(blank=True,null=True)
    start_date = models.DateTimeField(default=timezone.now)
    profile_image = models.ImageField(blank=True,null=True)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name','contact_no']

    def __str__(self):
        return self.user_name