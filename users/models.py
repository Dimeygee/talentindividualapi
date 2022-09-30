from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self,username,email,firstname,lastname,password=None,**extra_fields):
        if username is None:
            raise ValueError('Users must have username')

        if email is None:
            raise ValueError('Users must have an email address.')

        if firstname is None:
            raise ValueError('Users must have a firstname.')
        
        if lastname is None:
            raise ValueError('Users must have a lastname.')

        user = self.model(email=self.normalize_email(email),username=username,firstname=firstname,lastname=lastname,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,username,email,firstname,lastname,password=None,**extra_fields):
        user = self.create_user(email=self.normalize_email(email),username=username,firstname=firstname,lastname=lastname,password=password,**extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user 


class User(AbstractBaseUser, PermissionsMixin):
    SIGNUP_CHOICES = [
        (' ', '------'),
        ('talent', 'Talent'),
        ('recruiter', 'Recruiter'),
    ]
    JOBTYPE_CHOICES = [
        (' ', '------'),
        ('Digital & Design', 'Digital & Design'),
        ('Information Security / Cyber Security','Information Security / Cyber Security'),
        ('Project & Programme Management','Project & Programme Management'),
        ('Software Development & Engineering','Software Development & Engineering'),
        ('Technology Leadership', 'Technology Leadership'),
        ('Data & Analytics','Data & Analytics' ),
    ]
    JOBCONTRACT_CHOICES = [
        (' ', '------'),
        ('All', 'All'),
        ('Full-Time','Full-Time'),
        ('Part-Time','Part-Time'),
    ]
    username = models.CharField(db_index=True,max_length=50,unique=True, blank=True)
    email = models.EmailField(db_index=True,unique=True,blank=True) 
    firstname = models.CharField(max_length=50,blank=True) 
    lastname = models.CharField(max_length=50,blank=True) 
    signup_choices = models.CharField(max_length=512, choices=SIGNUP_CHOICES)
    cv= models.FileField(upload_to='cv',blank=True)
    jobType= models.CharField(max_length=512,choices=JOBTYPE_CHOICES)
    jobContract = models.CharField(max_length=512,choices=JOBCONTRACT_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['firstname',"lastname", "email"]

    objects = UserManager()

    def get_full_name(self):
        return f"{self.username}"

       

