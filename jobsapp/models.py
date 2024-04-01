from pyexpat import model
from this import d
from django.db import models
from django.forms import ModelMultipleChoiceField
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from tags.models import Tag

from .manager import JobManager

JOB_TYPE = (
    ("1", "Full time"),
    ("2", "Part time"),
    ("3", "Internship"),
    ("4", "Remotely"),
)
maincategory = (
    ("1", "developer"),
    ("2", "technology"),
    ("3", "accounting"),
    ("4", "medical"),
    ("5", "government"),
)



TrainginPlacementCategory = (
    ("1", "Training"),
    ("2", "Training&Certification"),
    ("3", "Placement"),
    ("4", "Traingin&Placement&Certification"),
   
)

class Job(models.Model):
    # jobImage=models.ImageField(upload_to='uploads/category', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    category = models.CharField(max_length=100)
    last_date = models.DateTimeField(null=True, blank=True)
    company_name = models.CharField(max_length=100)
    company_description = models.CharField(max_length=300)
    website = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    salary = models.CharField(max_length=100, default="")
    tags = models.ManyToManyField(Tag)
    opening=models.CharField(max_length=121,default=1)
    maincategory=models.CharField(choices=maincategory, max_length=10,default=1)
    experence=models.CharField(max_length=122,default="0-1 Year")
    phoneNumber=models.CharField(max_length=102,default="none")


    objects = JobManager()

    class Meta:
        ordering = ["id"]

    def get_absolute_url(self):
        return reverse("jobs:jobs-detail", args=[self.id])

    def __str__(self):
        return self.title


class Applicant(models.Model):
    # profileImage=models.ImageField(upload_to='uploads/category', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applicants")
    created_at = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)
    status = models.SmallIntegerField(default=1)
    primum=models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]
        unique_together = ["user", "job"]

    def __str__(self):
        return self.user.get_full_name()

    @property
    def get_status(self):
        if self.status == 1:
            return "Pending"
        elif self.status == 2:
            return "Accepted"
        else:
            return "Rejected"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(default=timezone.now)
    soft_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.job.title
class Contact(models.Model):
    name=models.CharField(max_length=300)
    subject=models.CharField(max_length=300)
    message=models.CharField(max_length=300)
    email=models.CharField(max_length=300)
class Blog1(models.Model):
    date=models.DateField()
    blogName =models.CharField(max_length=121)
    shortDesc =models.CharField(max_length=121)
    longDesc =models.CharField(max_length=121)
    status =models.CharField(max_length=121)
    blogUesrName=models.CharField(max_length=232)
    image = models.ImageField(upload_to='uploads/category', blank=True, null=True)
class BlogMain1(models.Model):
    date1=models.DateField()
    blogName1 =models.CharField(max_length=121)
    shortDesc1 =models.CharField(max_length=121)
    longDesc1 =models.CharField(max_length=121)
    status1 =models.CharField(max_length=121)
    blogUesrName1=models.CharField(max_length=232)
    image = models.ImageField(upload_to='uploads/category', blank=True, null=True)
class QuizAdminn(models.Model):
    email=models.CharField(max_length=232)
    password=models.CharField(max_length=121)

class BlogShow(models.Model):
    date2=models.DateField()
    blogName2 =models.CharField(max_length=121)
    shortDesc2 =models.CharField(max_length=121)
    longDesc2=models.CharField(max_length=121)
    status2 =models.CharField(max_length=121)
    blogUesrName2=models.CharField(max_length=232)
    image2 = models.ImageField(upload_to='uploads/category', blank=True, null=True)

class BlogShow1(models.Model):
    date21=models.DateField()
    blogName21 =models.CharField(max_length=121)
    shortDesc21 =models.CharField(max_length=121)
    longDesc21=models.CharField(max_length=121)
    status21 =models.CharField(max_length=121)
    blogUesrName21=models.CharField(max_length=232)
    image21 = models.ImageField(upload_to='uploads/category', blank=True, null=True)


class MainBlog(models.Model):
    blogdate=models.DateField()
    name =models.CharField(max_length=1211)
    desc1short =models.CharField(max_length=1211)
    decs2long=models.CharField(max_length=1121)
    blogStatus =models.CharField(max_length=1211)
    usernameBlog=models.CharField(max_length=2312)
    imageBlog = models.ImageField(upload_to='uploads/category', blank=True, null=True)

class CheckoutMmeber(models.Model):
    fname=models.CharField(max_length=121)
    lname=models.CharField(max_length=121)
    cname=models.CharField(max_length=121)
    streed=models.CharField(max_length=121)
    city=models.CharField(max_length=121)  
    state=models.CharField(max_length=121)
    pin=models.CharField(max_length=121)
    phone=models.CharField(max_length=121)
    email=models.CharField(max_length=121)
    paymentDone=models.BooleanField(default=False)


class TrainCertPlacement(models.Model):
    image = models.ImageField(upload_to='uploads/category', blank=True, null=True)
    Category=models.CharField(choices=TrainginPlacementCategory, max_length=10,default=1)
    title=models.CharField(max_length=121)
    price=models.CharField(max_length=121)
    disc=models.CharField(max_length=121)
    feature1=models.CharField(max_length=121)
    featured2=models.CharField(max_length=121)
    featured3=models.CharField(max_length=121)
    featured4=models.CharField(max_length=121)
    featured5=models.CharField(max_length=121)
    featured6=models.CharField(max_length=121)
    skill=models.CharField(max_length=121)
    benifits=models.CharField(max_length=121)
    Technology=models.CharField(max_length=121)

class DoucmentEmpMain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    companyIdCard=models.FileField(upload_to='uploads/category', blank=True, null=True)
    shopStablished=models.FileField(upload_to='uploads/category', blank=True, null=True)
    udyogAAdhar=models.FileField(upload_to='uploads/category', blank=True, null=True)
    certificateOfIncorpation=models.FileField(upload_to='uploads/category', blank=True, null=True)
    msmacertificate=models.FileField(upload_to='uploads/category', blank=True, null=True)
    Tan=models.FileField(upload_to='uploads/category', blank=True, null=True)
    Din=models.FileField(upload_to='uploads/category', blank=True, null=True)
    verified=models.BooleanField(default=False)
    def __str__(self):
        return self.user.email