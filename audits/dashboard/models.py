from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class Audits(models.Model):
    _id=models.CharField(max_length=100)
    type=models.CharField(max_length=100)
    severity=models.CharField(max_length=100)
    summary=models.CharField(max_length=100)
    appd_application_name=models.CharField(max_length=100)
    timestamp=models.IntegerField()
    date=models.DateTimeField()
    eventTime=models.CharField(max_length=100)

    class Meta:
        db_table ="appd_events_audit" #appd_events_audit, test_data





class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    
    objects = UserManager()


