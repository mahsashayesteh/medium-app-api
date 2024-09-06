from django.contrib.auth import get_user_model
from django.db import models
from core_apps.common.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


User = get_user_model()

class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = "M",_("مرد")
        FEMAIL = "F", _("خانم")
    
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    phonenumber = models.CharField( max_length=15)
    about_me = models.TextField(verbose_name=_("درباره من"), 
                                default="یادداشت کنید")
    gender = models.CharField(verbose_name=_("جنسیت"),
                              choices=Gender.choices,
                              default=Gender.MALE,
                              max_length=30)
    country = CountryField(verbose_name =_("کشور"), max_length=50 )
    city = models.CharField(
        verbose_name=_("شهر"),max_length=50,default=_("تهران"), blank=False, null=False,
        )
    profile_photo = models.ImageField(
        verbose_name=_("عکس پروفایل"), default="/profile_photo"
        )
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", blank=True
        )
    
    def __str__(self) :
        return f"{self.user.first_name}"
    
    def follow(self, profile):
        return self.followers.add(profile)
    
    def unfollow(self, profile):
        return self.followers.remove(profile)
    
    def check_followers(self, profile):
        return self.followers.filter(pkid=profile.pkid).exists()
