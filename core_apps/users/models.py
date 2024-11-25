import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .manager import CustomeUserManager

class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(verbose_name=_("نام کاربری"), db_index=True, 
                                max_length=255, default="username")
    first_name = models.CharField(verbose_name=_("نام"), max_length=50)
    last_name = models.CharField(verbose_name=_("نام خانوادگی"), max_length=50)
    email = models.EmailField(verbose_name=_("ایمیل"), unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomeUserManager()

    class Meta:
        verbose_name = _("کاربر")
        verbose_name_plural = _("کاربران")
    
    def __str__(self):
        return self.email
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.first_name
    