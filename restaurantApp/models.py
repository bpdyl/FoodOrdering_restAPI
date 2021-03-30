from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.

def upload_to(instance, filename):
    return 'restaurants/{filename}'.format(filename=filename)

class restaurantModel(models.Model):

    class RestaurantObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status = 'open')

    options = (
        ('closed','Close'),
        ('open','Open'),
    )
    root_usr = models.OneToOneField(settings.AUTH_USER_MODEL,null=True, on_delete=models.CASCADE, related_name='restaurants')
    rest_name = models.CharField(max_length = 1000,)
    rest_email = models.EmailField(max_length=200,null=True)
    rest_owner_name = models.CharField(max_length = 1000,null = True, blank = True)
    rest_phone = models.IntegerField(null = True, blank = True)
    rest_address = models.CharField(max_length = 10000, null = True, blank = True)
    rest_area = models.CharField(max_length = 1000, null = True, blank = True)
    slug = models.SlugField(max_length = 250, unique_for_date ='rest_reg_date')
    rest_city = models.CharField(max_length = 1000, null = True, blank = True)
    rest_country = models.CharField(max_length = 1000, null = True, blank = True)
    rest_opentime = models.TimeField(null = True, blank = True)
    rest_closetime = models.TimeField(null = True, blank = True)
    rest_image = models.ImageField(_("Image"), upload_to=upload_to,default='restaurants/default.jpg', null = True, blank = True)
    rest_reg_date = models.DateTimeField()
    status = models.CharField(max_length=10,choices = options, default = 'open')
    rest_description = models.CharField(max_length = 10000, null = True, blank = True)
    rest_merchant_id = models.IntegerField(null = True, blank = True)
    is_verified = models.BooleanField(default = False),
    objects = models.Manager() #default manager
    restobjects = RestaurantObjects() #custom manager

    class Meta:
        ordering = ('rest_reg_date',)

    def __str__(self):
        return self.rest_name

class restMenuModel(models.Model):
    restaurant = models.OneToOneField(restaurantModel,null = True, on_delete = models.CASCADE)
    Menu = models.CharField(max_length = 3000)

    def __str__(self):
        return self.Menu + " " + str(self.restaurant)
class restFoodModel(models.Model):
    restaurant = models.OneToOneField(restaurantModel,null = True, on_delete = models.CASCADE,related_name='foods')
    slug = models.SlugField(db_index=False,null = True)
    Menu = models.OneToOneField(restMenuModel,null = True, on_delete = models.CASCADE)
    food_name = models.CharField(max_length = 3000)
    food_image = models.ImageField(max_length = 5000, null = True, blank = True)
    food_description = models.CharField(max_length = 10000, null = True, blank = True)
    food_price = models.PositiveIntegerField()

    class Meta:
        unique_together = (('slug','Menu','restaurant'),)

    def __str__(self):
        return self.food_name + "  " + str(self.restaurant)

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug':self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug':self.slug
        })
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug':self.slug
        })
