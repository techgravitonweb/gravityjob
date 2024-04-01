from re import L
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from accounts.managers import UserManager

GENDER_CHOICES = (("male", "Male"), ("female", "Female"))


class User(AbstractUser):
    username = None
    role = models.CharField(max_length=12, error_messages={"required": "Role must be provided"})
    gender = models.CharField(max_length=10, blank=True, null=True, default="")
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    premium=models.BooleanField(default=False)

    def __unicode__(self):
        return self.email

    objects = UserManager()

maincategory = (
    ("1", "developer"),
    ("2", "technology"),
    ("3", "accounting"),
    ("4", "medical"),
    ("5", "government"),
)
class FullDetailEmployer(models.Model):
    employerData=models.ForeignKey(User, on_delete=models.CASCADE)
    profileImage=models.ImageField(upload_to='uploads/category', blank=True, null=True)
    coverPic=models.ImageField(upload_to='uploads/category', blank=True, null=True)
    employerName=models.CharField(max_length=121)
    Email=models.CharField(max_length=121)
    phoneNumber=models.CharField(max_length=121)
    website=models.CharField(max_length=121)
    compnaySize=models.CharField(max_length=121)
    category=models.CharField(choices=maincategory, max_length=10,default=1)
    indroductionVideoUrl=models.CharField(max_length=121)
    aboutCompany=models.CharField(max_length=121)
    subLeadMemberName=models.CharField(max_length=121)
    subLeadMemberDesination=models.CharField(max_length=121)
    subLeadMemberExperience =models.CharField(max_length=121)
    location=models.CharField(max_length=121)
    socailNetwork =models.CharField(max_length=121)
class FullDetailEmploye(models.Model):
    employeeData=models.ForeignKey(User, on_delete=models.CASCADE)
    profileImgae=models.ImageField(upload_to='uploads/category', blank=True, null=True)
    fullName=models.CharField(max_length=121)
    email=models.CharField(max_length=121)
    phoneNumber=models.CharField(max_length=121)
    age=models.CharField(max_length=121)
    gender=models.CharField(max_length=121)
    qualification=models.CharField(max_length=121)
    language=models.CharField(max_length=121)
    jobTitle=models.CharField(max_length=121)
    experienceTime=models.CharField(max_length=121)
    salaryType=models.CharField(max_length=121)
    categories=models.CharField(max_length=121)
    portfolioLink=models.CharField(max_length=121)
    location=models.CharField(max_length=121)
    address=models.CharField(max_length=121)
    socialNetwork=models.CharField(max_length=121,default="google.com")
# class Resume(models.Model):
#     # employeeData=models.ForeignKey(User, on_delete=models.CASCADE)
#     resume=models.FileField(upload_to='uploads/category')
#     PortfolioUrl=models.CharField(max_length=121,default="shios")
#     Data=models.ForeignKey(User, on_delete=models.CASCADE,default=1)

class Resumeshow(models.Model):
    # employeeData=models.ForeignKey(User, on_delete=models.CASCADE)
    resume1=models.FileField(upload_to='uploads/category')
    PortfolioUrl1=models.CharField(max_length=121,default="shios")
    Data1=models.ForeignKey(User, on_delete=models.CASCADE)


class NewsLetter(models.Model):
    email=models.CharField(max_length=121,default="shios")
    phone=models.CharField(max_length=121,default="123")
    