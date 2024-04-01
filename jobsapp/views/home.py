from datetime import datetime
from queue import Full
import re

from unicodedata import name
from wsgiref.util import request_uri
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView
from rest_framework.decorators import api_view
from django.views.generic.base import View
from sqlalchemy import false
from accounts.models import *
import math
import random
from tags.models import Tag
from ..documents import JobDocument
from ..forms import ApplyJobForm
from ..models import *
from ..models import Job as JobModel
from django.db.models import Q
from .employer import *
from quiz.views import *
from quiz.urls import *
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from jobs import settings
import json
import razorpay
import requests
from django.core.files.storage import FileSystemStorage
from .ccavutil import encrypt,decrypt
from .ccavResponseHandler import res
from string import Template
from django.http import HttpResponse


accessCode = 'AVTR82JE25BN28RTNB' 	
workingKey = '2E46D0BA92D97F064B04C0C3F4B73598'

def HomeView(request):
    context={}
    s=Job.objects.all()
    for x in s:
        print(x.pk)
    context["trendings"] = Job.objects.all()[0:3]
    print("trending value",context["trendings"])
    context["tags"]=Tag.objects.all()[:6]
    context["company"]=Job.objects.all()[0:10]
    print(Job.objects.all().count())
    companyList=[]
    for x in context["company"]:
        if x.company_name not in companyList:
            companyList.append(x.company_name)
    context["company1"]=companyList
    context["featured1"]=Job.objects.filter(Q(type="1") | Q(type="3"))[0:4]
    context["featured2"]=Job.objects.filter(Q(type="1") | Q(type="3"))[5:8]
    print(context["featured2"])
    context["featured3"]=Job.objects.filter(Q(type="1") | Q(type="3"))[9:12]
    for x in context['featured1']:
        if x.type=="1":
            x.type="fullTime"
        else:
            x.type="Intership"
    for x in context['featured2']:
        if x.type=="1":
            x.type="fullTime"
        else:
            x.type="Intership"
    for x in context['featured3']:
        if x.type=="1":
            x.type="fullTime"
        else:
            x.type="Intership"
    context["remotly1"]=Job.objects.filter(type="4")[0:4]
    context["remotly2"]=Job.objects.filter(type="4")[5:8]
    context["remotly3"]=Job.objects.filter(type="4")[9:12]
    context["location"]=Job.objects.all().distinct()
    for x in context["remotly1"]:
        x.type="Remotly"
    for x in context["remotly2"]:
        x.type="Remotly"
    for x in context["remotly3"]:
        x.type="Remotly"
    context["partTime1"]=Job.objects.filter(type="2")[0:4]
    context["partTime2"]=Job.objects.filter(type="2")[5:8]
    context["partTime3"]=Job.objects.filter(type="2")[9:12]
    for x in context["partTime1"]:
        x.type="Part Time"
    for x in context["partTime2"]:
        x.type="Part Time"
    for x in context["partTime3"]:
        x.type="Part Time"
    context["fullTime1"]=Job.objects.filter(type="1")[0:5]
    context["fullTime2"]=Job.objects.filter(type="1")[7:12]
    print(context["fullTime2"])
    context["fullTime3"]=Job.objects.filter(type="1")[13:17]
    for x in context["fullTime1"]:
        x.type="Full Time"
    for x in context["fullTime2"]:
        x.type="Full Time"
    for x in context["fullTime3"]:
        x.type="Full Time"
    ## end of post job code 
    ##location list 
    context["company"]=Job.objects.all()
    CompanyList=[]
    primarykeys=[]
    context["primumCandidates"]=User.objects.filter(premium=True).filter(role="employee")
    print("###@@@primus context value",context["primumCandidates"])
    for x in context["company"]:
        if x.company_name not in CompanyList:
            CompanyList.append(x.company_name)
            primarykeys.append(x.pk)
    context["company"]=Job.objects.filter(pk__in=primarykeys)
    locationList=[]
    primarykeys=[]
    context['location']=Job.objects.all()
    for x in context["location"]:
        if x.location not in locationList:
            locationList.append(x.location)
            primarykeys.append(x.pk)
    context["location"]=Job.objects.filter(pk__in=primarykeys)
    
    # context["location"]=locationList
    return render(request,"jobPortal/index.html",context)

class SearchView(ListView):
    model = Job
    template_name = "jobPortal/listing_right.html"
    context_object_name = "jobs"

    def get_queryset(self):
        return self.model.objects.filter(
            location__contains=self.request.GET.get("location", ""),
            title__contains=self.request.GET.get("position", ""),)



def JobListView(request):
    context={}
    context["jobs"]=Job.objects.all()
    context["location"]=Job.objects.all()
    context["company"]=Job.objects.all()
    for x in context["location"]:
        locationList=[]
        primarykeys=[]
    for x in context["location"]:
        if x.company_name not in locationList:
            locationList.append(x.company_name)
            primarykeys.append(x.pk)
    context["location"]=Job.objects.filter(pk__in=primarykeys)
    for x in context["location"]:
        CompanyList=[]
        primarykeys=[]
    for x in context["company"]:
        if x.company_name not in CompanyList:
            CompanyList.append(x.company_name)
            primarykeys.append(x.pk)
    context["company"]=Job.objects.filter(pk__in=primarykeys)    
    return render(request,"jobPortal/listing_right.html",context)


class JobDetailsView(DetailView):
    model = Job
    template_name = "jobPortal/listing_single.html"
    context_object_name = "job"
    pk_url_kwarg = "id"

    def get_object(self, queryset=None):
        obj = super(JobDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # raise error
            raise Http404("Job doesn't exists")
        context = self.get_context_data(object=self.object)
        jobsStore=context["job"]
        print(jobsStore.tags)
        print("request.user checking",self.request.user)
        if self.request.user.is_authenticated:
            if self.request.user.role=="employer":
                jobauth=Job.objects.get(pk=jobsStore.id)
                print("id of the user",self.request.user.id)
                print("id of the job user",jobauth.user.id)
                if self.request.user.id == jobauth.user.id:
                    context["editauth"]=True
                else:
                    context["editauth"]=None
                print("going in if request.user checking ")
                context["is_applied"]=None
            else:
                context["is_applied"]=Applicant.objects.filter(user=request.user,job_id=jobsStore.id)
                print(context["is_applied"])
                if context["is_applied"] :
                    context["is_applied"]=True
                else:
                    context["is_applied"]=None
                print("context value printing",context["is_applied"])
        else:
            context["is_applied"]=None
            context["editauth"]=None
        print(context["is_applied"])
        return self.render_to_response(context)


class ApplyJobView(CreateView):
    model = Applicant
    form_class = ApplyJobForm
    slug_field = "job_id"
    slug_url_kwarg = "job_id"

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, "Successfully applied for the job!")
            return self.form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy("jobs:home"))

    def get_success_url(self):
        return reverse_lazy("jobs:jobs-detail", kwargs={"id": self.kwargs["job_id"]})



    def form_valid(self, form):
        # check if user already applied
        applicant = Applicant.objects.filter(user_id=self.request.user.id, job_id=self.kwargs["job_id"])
        if applicant:
            messages.info(self.request, "You already applied for this job")
            return HttpResponseRedirect(self.get_success_url())
        # save applicant
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


def favorite(request):
    if not request.user.is_authenticated:
        return JsonResponse(data={"auth": False, "status": "error"})

    job_id = request.POST.get("job_id")
    user_id = request.user.id
    try:
        fav = Favorite.objects.get(job_id=job_id, user_id=user_id, soft_deleted=False)
        if fav:
            fav.soft_deleted = True
            fav.save()
            # fav.delete()
            return JsonResponse(
                data={
                    "auth": True,
                    "status": "removed",
                    "message": "Job removed from your favorite list",
                }
            )
    except Favorite.DoesNotExist:
        Favorite.objects.create(job_id=job_id, user_id=user_id)
        return JsonResponse(
            data={
                "auth": True,
                "status": "added",
                "message": "Job added to your favorite list",
            }
        )



class HomeView1(View):
    def get(self, request, *args, **kwargs):
        return render(request, "dash/chart.html")



class testCandidate(View):
    def get(self, request, *args, **kwargs):
        print("goint inside the page")
        print(self.request.user)
        data=Resumeshow.objects.filter(Data1=request.user)
        if data.exists():
            resumeshow=True
        else:
            resumeshow=None
        if not self.request.user.is_authenticated:
            print("checking login")
            return redirect("accounts:login") 
        print("checking end of that")
        s=FullDetailEmploye.objects.filter(employeeData=request.user)
        jobs=Job.objects.all()[0:3]
        fullTime1=Job.objects.filter(type="1")[0:5]
        applied=Applicant.objects.filter(user=request.user)
        shortlisted=Applicant.objects.filter(user=request.user,status=2)
        appliedCount=applied.count()
        shortlistedCount=shortlisted.count()
        context={"s":s,"jobs":jobs,"fullTime1":fullTime1,"appliedCount":appliedCount,"shortlistedCount":shortlistedCount,'resumeshow':resumeshow}
        return render(request, "dash/user/dashboard.html",context)



def member(request):
    return render(request, "jobPortal/pricing.html")
        
class blog(View):
    def get(self, request, *args, **kwargs):
        company=Job.objects.all()
        print("@@company",company)
        userBlogList=MainBlog.objects.all()
        context={"userBlogList":userBlogList,"company":company}
        return render(request, "jobPortal/blog_right.html",context)

class contact(View):
    def post(self, request, *args, **kwargs):
        message=None
        if request.method=="POST":
            name=request.POST['name']
            message=request.POST['message']
            subject=request.POST['subject']
            email=request.POST['email']
            m=Contact.objects.create(name=name,message=message,email=email,subject=subject)
            m.save()
            message="We will contact you soon .Please be Patience"
            context={'message':message}
            return render(request,'jobPortal/contact.html',context)
    def get(self, request, *args, **kwargs):
        return render(request, "jobPortal/contact.html")

class about(View):
    def get(self, request, *args, **kwargs):
        return render(request, "jobPortal/about.html")


def profile(request):
    s=FullDetailEmploye.objects.filter(employeeData=request.user)
    data=Resumeshow.objects.filter(Data1=request.user)
    if data.exists():
        resumeshow=True
    else:
        resumeshow=None
    if s.exists():
        profileShow=True
        profiledata=s
    else:
        profileShow=None
        print('value is going here ...........................................................')
        profiledata=None
    if request.method=="POST":
        if "PortfolioUrl" in  request.POST:
            resume=request.FILES['resume1']
            PortfolioUrl=request.POST["PortfolioUrl"]
            s=Resumeshow.objects.filter(resume1=resume)
            if s:
                print("already exist")
            else:
                s=Resumeshow.objects.create(resume1=resume,PortfolioUrl1=PortfolioUrl,Data1=request.user)
                resumeshow=True
                s.save()   
        else:  
            employeeData=request.user
            profileImgae=request.FILES["profileImgae"]
            fullName=request.POST["fullName"]
            email=request.POST["email"]
            phoneNumber=request.POST["phoneNumber"]
            age=request.POST["age"]
            gender=request.POST["gender"]
            qualification=request.POST["qualification"]
            language=request.POST["language"]
            jobTitle=request.POST["jobTitle"]
            experienceTime=request.POST["experienceTime"]
            salaryType=request.POST["salaryType"]
            categories=request.POST["categories"]
            socialNetwork=request.POST["socialNetwork"]
            location=request.POST["location"]
            address=request.POST["address"]
            s=FullDetailEmploye.objects.filter(employeeData_id=request.user)
            profileShow=True
            if s:
                s.employeeData,s.profileImgae,s.fullName,s.email,s.phoneNumber,s.age,s.gender,s.qualification,s.language,s.jobTitle,s.experienceTime,s.salaryType,s.categories,s.socialNetwork,s.location,s.address=employeeData,profileImgae,fullName,email,phoneNumber,phoneNumber,age,gender,qualification,language,jobTitle,experienceTime,salaryType,categories,socialNetwork,location,address
                s.save()
            else:
                s1=FullDetailEmploye.objects.create(employeeData=employeeData,profileImgae=profileImgae,fullName=fullName,email=email,phoneNumber=phoneNumber,age=age,gender=gender,qualification=qualification,language=language,jobTitle=jobTitle,experienceTime=experienceTime,salaryType=salaryType,categories=categories,socialNetwork=socialNetwork,location=location,address=address)
                s1.save()
    context={"profileShow":profileShow,
    "profiledata":profiledata,
    "resumeshow":resumeshow}
    return render(request, "dash/user/profile.html",context)


class table(View):
    def get(self, request, *args, **kwargs):
        return render(request, "dash/user/tables.html")

class billing(View):
    def get(self, request, *args, **kwargs):
        context={}
        context['jobs']=Applicant.objects.filter(user=request.user).filter(status=2)
        print("cheking the data",context["jobs"])
        return render(request, "dash/user/billing.html",context)

def changePassword(request):
    passwordValue=None
    if request.method=="POST":
        if "old2" in request.POST:
            new=request.POST["new2"]
            s=User.objects.get(email=request.user.email)
            s.set_password(new)
            s.save()
            passwordValue=True
        else:
            old=request.POST["new1"]
            new=request.POST["new"]
            s1=request.session["email"]
            s=User.objects.get(email=s1)
            s.set_password(new)
            s.save()
            passwordValue=True
            return redirect("jobs:employer-dashboard")
    context={"passwordValue":passwordValue}
    if request.user.is_authenticated and request.user.role == 'employer':
        print("employerr")
        return render(request,"dash/user/changePassword.html")
    elif  request.user.is_authenticated and request.user.role == 'employee': 
        print("employee")
        return render(request,"dash/user/changepasswordEmployee.html")




def blogShow(request,pk):
    print("print the pk",pk)
    s=MainBlog.objects.get(pk=pk)
    category=Job.objects.all().distinct() 
    featured1=Job.objects.filter(Q(type="1") | Q(type="3"))[0:5]   
    if True:
        context={"x":s,
        "category":category,
        "featured1":featured1
        }
        return render(request, 'jobPortal/blog_single_right.html',context)    
    return render(request, 'jobPortal/blog_single_right.html')

def updateEmployer(request):
    print("userdetails ",request.user)
    try:
        s =FullDetailEmployer.objects.get(employerData=request.user)
    except:
        s=None
    if request.method=="POST":
        employerData=request.user
        if "employprofileImageerData" not in request.POST:
            profileImage=s.profileImage.url
            coverPic=s.coverPic.url
            print("@@employer profile checking")
        else:
            profileImage=request.FILES["employprofileImageerData"] 
            coverPic=request.FILES["coverPic"]
        employerName=request.POST["employerName"]
        Email=request.POST["Email"]
        phoneNumber=request.POST["phoneNumber"]
        website=request.POST["website"]
        compnaySize="n"
        category=request.POST["category"]
        indroductionVideoUrl="indroductionVideoUrl"
        aboutCompany=request.POST["aboutCompany"]
        subLeadMemberName="subLeadMemberName"
        subLeadMemberDesination="subLeadMemberName"
        subLeadMemberExperience ="subLeadMemberName"
        location=request.POST["location"]
        socailNetwork =request.POST["socailNetwork"]
        try:
            s=FullDetailEmployer.objects.get(employerData_id=request.user)
        except:
            s=None
        if s is not None:
            s.employerName=employerName
            s.Email=Email
            s.phoneNumber=phoneNumber
            s.website=website
            s.compnaySize=compnaySize
            s.category=category
            s.indroductionVideoUrl=indroductionVideoUrl
            s.aboutCompany=aboutCompany
            s.subLeadMemberName=subLeadMemberName
            s.subLeadMemberDesination=subLeadMemberDesination
            s.subLeadMemberExperience=subLeadMemberExperience
            s.location=location
            s.socailNetwork=socailNetwork
            s.save()
            print("@@employer profile checking")
        else:
            s1=FullDetailEmployer.objects.create(employerData=employerData,profileImage=profileImage,coverPic=coverPic,employerName=employerName,Email=Email,phoneNumber=phoneNumber,website=website,compnaySize=compnaySize,category=category,indroductionVideoUrl=indroductionVideoUrl,aboutCompany=aboutCompany,subLeadMemberName=subLeadMemberName,subLeadMemberDesination=subLeadMemberDesination,subLeadMemberExperience=subLeadMemberExperience,location=location,socailNetwork=socailNetwork)
            print("@@employer profile checking121")
            s1.save()
    return  redirect('jobs:employer-dashboard')


def changePasswordEmp(request):
    if request.method=="POST":
        old=request.POST["old"]
        new=request.POST["new"]
        s=User.objects.get(email=request.user.email)
        s.set_password(new)
        s.save()
        print("it is going inside")
    return redirect('accounts:login')

def postjobDash(request):
    return render(request,"dash/user/postjobDash.html")
def viewProfile(request):
    context={}
    data =FullDetailEmployer.objects.filter(employerData=request.user)
    # print("checking that is exist",s)
    if data.exists():
        print("exist")
        context["checkUserDetails"]=True
    else:
        context["checkUserDetails"]=None
    print("employer profile data",data)
    context["data"]=data
    return render(request,"dash/user/viewProfile.html",context)
def companyProfile(request):
    context={}
    s=FullDetailEmployer.objects.filter(employerData=request.user)
    print("value of s",s)
    context["data"]= s
    print("checking that is exist",s)
    if s.exists():
        print("exist")
        context["checkUserDetails"]=True
    else:
        context["checkUserDetails"]=None
    if request.user.is_authenticated and request.user.role == 'employer':
        return render(request,"dash/user/companyProfile.html",context)
def changepassword(request):
    return render(request,"dash/user/changepassword.html")
   
def postjob(request):
    messagePost=None
    if request.method=='POST':
        print(request.user)
        user = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        location = request.POST["location"]
        type = request.POST["type"]
        category = request.POST["category"]
        if "last_date" not in request.POST:
            last_date=None
        else:
            last_date =request.POST["last_date"]
        company_name = request.POST["company_name"]
        company_description = request.POST["company_description"]
        if "website" not in request.POST:
            website = 'none'
        else:
            website = request.POST["website"]
        created_at = datetime.now()
        filled =False
        if "minSalarylakh" not in request.POST:
            salary="salary disclosed Later"
        else:
            minSalarylakh =request.POST["minSalarylakh"]
            minSalarythousand =request.POST["minSalarythousand"]
            maxSalarythousand =request.POST["maxSalarythousand"]
            maxSalarylakh =request.POST["maxSalarylakh"]
            salary=minSalarylakh+","+minSalarythousand+"To"+maxSalarylakh+","+maxSalarythousand
        print("salary value ",salary)
        tags=1 
        opening="100"
        maincategory=request.POST["maincategory"]
        experence=request.POST["experence"]
        s=Job.objects.create(user=user,title=title,description=description,location=location,type=type,category=category,last_date=last_date,company_name=company_name,company_description=company_description,website=website,created_at=created_at,filled=filled,salary=salary,opening=opening,maincategory=maincategory,experence=experence)
        s1=Tag.objects.create(name="Django")
        s.tags.add(s1)
        s.save()
        messagePost=True
        context={"messagePost":messagePost}
        return render(request, "dash/user/postjobDash.html",context)
    context={"messagePost":messagePost}
    return render(request, "jobPortal/postjob.html",context)



def candidates(request):
    context={}
    context["location"]=Job.objects.all()
    context["company"]=Job.objects.all()
    context["tags"]=Tag.objects.all()[:6]
    context["applicant"]=User.objects.filter(role="employee")
    for x in context["location"]:
        locationList=[]
        primarykeys=[]
    for x in context["location"]:
        if x.company_name not in locationList:
            locationList.append(x.company_name)
            primarykeys.append(x.pk)
    context["location"]=Job.objects.filter(pk__in=primarykeys)
    for x in context["location"]:
        CompanyList=[]
        primarykeys=[]
    for x in context["company"]:
        if x.company_name not in CompanyList:
            CompanyList.append(x.company_name)
            primarykeys.append(x.pk)
    context["company"]=Job.objects.filter(pk__in=primarykeys) 
    if request.user.is_authenticated and request.user.role == 'employer':  
        if request.user.role=="employer": 
            return render(request,"jobPortal/candidate_listing.html",context)
    else:
        return redirect("accounts:login")        





def candidatesFull(request,pk):
    try:
        employeeDetailss=FullDetailEmploye.objects.get(employeeData_id=pk)
    except:
        employeeDetailss=None
    try:
        resume=Resumeshow.objects.get(Data1_id=pk)
    except:
        resume=None
    print("employee details is showing their",employeeDetailss)
    context={"employeeDetailss":employeeDetailss,
    "resume":resume}
    print(context)
    print("employee details is showing their",employeeDetailss)
    return render(request, 'jobPortal/candidate_profile.html',context)

def shortValueCompany(request,pk):
    x=Job.objects.get(pk=pk)
    context={}
    context["jobs"]=Job.objects.filter(company_name=x.company_name)
    context["location"]=Job.objects.all()
    context["company"]=Job.objects.all()
    context["type"] = Job.objects.all()
    for x in context["location"]:
        locationList=[]
        primarykeys=[]
    for x in context["location"]:
        if x.company_name not in locationList:
            locationList.append(x.company_name)
            primarykeys.append(x.pk)
    context["location"]=Job.objects.filter(pk__in=primarykeys)
    for x in context["location"]:
        CompanyList=[]
        primarykeys=[]
    for x in context["company"]:
        if x.company_name not in CompanyList:
            CompanyList.append(x.company_name)
            primarykeys.append(x.pk)
    context["company"]=Job.objects.filter(pk__in=primarykeys)
    for x in context["type"]:
        locationList=[]
        primarykeys=[]
    for x in context["type"]:
        if x.company_name not in locationList:
            locationList.append(x.company_name)
            primarykeys.append(x.pk)
    context["type"]=Job.objects.filter(pk__in=primarykeys)    
    return render(request,"jobPortal/listing_right.html",context)
    # context={}
    # context['jobs']=Job.objects.filter(company_name=x.company_name)
    # return render(request,'jobPortal/listing_right.html',context)

def shortValueLocation(request,pk):
    context={}
    context["company"]=Job.objects.all()
    CompanyList=[]
    primarykeys=[]
    for x in context["company"]:
        if x.company_name not in CompanyList:
            CompanyList.append(x.company_name)
            primarykeys.append(x.pk)
    context["company"]=Job.objects.filter(pk__in=primarykeys)
    locationList=[]
    primarykeys=[]
    context['location']=Job.objects.all()
    for x in context["location"]:
        if x.location not in locationList:
            locationList.append(x.location)
            primarykeys.append(x.pk)
    context["location"]=Job.objects.filter(pk__in=primarykeys)
    print("pringing",pk)
    x=Job.objects.get(pk=pk)
    print("location value",x)
    
    context['jobs']=Job.objects.filter(location=x.location)
    return render(request,'jobPortal/listing_right.html',context)

def shortValueTag(request,pk):
    x=Tag.objects.get(pk=pk)
    print("value of tags",x.name)
    context={}
    all=[]
    s=Job.objects.filter(location="fdjiofsdj")
    print("s")
    jobs=Job.objects.all()
    for y in jobs:
        print(y.tags.all())
        if y.tags.all():
            for z in y.tags.all():
                if x.name==z.name:
                    al=Job.objects.filter(title=y.title)
                    s=s.union(al)
                    break
    print("tags value",all)
    context["jobs"]=all
    context["company"]=Job.objects.all()
    CompanyList=[]
    primarykeys=[]
    for x in context["company"]:
        if x.company_name not in CompanyList:
            CompanyList.append(x.company_name)
            primarykeys.append(x.pk)
    context["company"]=Job.objects.filter(pk__in=primarykeys)
    locationList=[]
    primarykeys=[]
    context['location']=Job.objects.all()
    for x in context["location"]:
        if x.location not in locationList:
            locationList.append(x.location)
            primarykeys.append(x.pk)
    context["location"]=Job.objects.filter(pk__in=primarykeys)
    # context['jobs']=Job.objects.filter(tags=x.name)
    print("tagging value checking",context['jobs'])
    
    return render(request,'jobPortal/listing_right.html',context)
def Home(request):
    trendings = Job.objects.all()[3:6]
    context={"trendings":trendings}
    return render(request,"jobPortal/index.html",context)
def QuizAdmin(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        # s=QuizAdminn.objects.filter(email=email,password=password)
        # if s:
        #     form = CreateQuizForm()
        #     context = {
        #             'form': form,}
        form = CreateQuizForm()
        context = {
                     'form': form,}
        return render(request, 'quiz/create_quiz.html', context)
    return render(request,"QuizAdmin.html")
def category(request,value):
    print(value)
    context={}
    context["jobs"]=Job.objects.filter(maincategory=value)
    context["company"]=Job.objects.all()
    CompanyList=[]
    primarykeys=[]
    for x in context["company"]:
        if x.company_name not in CompanyList:
            CompanyList.append(x.company_name)
            primarykeys.append(x.pk)
    context["company"]=Job.objects.filter(pk__in=primarykeys)
    locationList=[]
    primarykeys=[]
    context['location']=Job.objects.all()
    for x in context["location"]:
        if x.location not in locationList:
            locationList.append(x.location)
            primarykeys.append(x.pk)
    context["location"]=Job.objects.filter(pk__in=primarykeys)
    return render(request,'jobPortal/listing_right.html',context)

def terms(request):
    return render(request,"jobPortal/terms&condition.html")

def email(request):
    message=None
    if request.method=="POST":
        if "phone" in request.POST:
            phone=request.POST["phone"]
        else:
            phone="need to enter "
        if "email" in request.POST:
            email=request.POST["email"]
        else:
            email="need to enter "
        s=NewsLetter.objects.create(email=email,phone=phone)
        s.save()
        message="We will contact you soon .Please be Patience"
        print(message)
    context={"message":message}
    return render(request,"jobPortal/success.html",context)


def memberplan(request):
    if request.method=="POST":
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        cname=request.POST["cname"]
        streed=request.POST["streed"]
        city=request.POST["city"]
        state=request.POST["state"]
        pin=request.POST["pin"]
        phone=request.POST["phone"]
        email=request.POST["email"]
        s=CheckoutMmeber.objects.create(fname=fname,lname=lname,cname=cname,streed=streed,state=state,city=city,pin=pin,phone=phone,email=email,paymentDone=False)
        s.save()
        request.session["id"]=s.id
        amount =request.POST["amount"]
        amount=int(amount)
        amount=amount*100
        print("ammount value",amount)
        order_currency = 'INR'
        client=razorpay.Client(
	        auth=('rzp_test_jo7a3gIXrGmxcH','DfoVMYjJS3mKNoz5Tn6BzciY'))
        payment=client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
        context={'amount':amount,'payment':payment}
        return render(request,"jobPortal/payment-page.html",context)

def forgetPassword(request):
    return render(request,"jobPortal/forgetPassword.html")
    

def userPassword(request):
    otpCheck=None 
    emailCheck=None
    emailForm=True
    otpForm=None
    if request.method=='POST':
        if "email" in request.POST:
            email=request.POST["email"]
            request.session["email"]=email
            if User.objects.filter(email=email).exists():
                otpForm,emailForm=True,None
                digits = [i for i in range(0, 10)]
                random_str = ""
                for i in range(6):
                    index = math.floor(random.random() * 10)
                    random_str += str(digits[index])
                    print(random_str)
                    request.session['otp']=random_str
                #mail sending on the server
                # subject="Thenewshoppinghub.com/order form "
                # context={'random_str':random_str,'email':email} 
                # print("checking after context   ")
                # html_message=render_to_string('jobPortal/main_template.html',context)
                # plain_message = strip_tags(html_message)
                # email_from=settings.EMAIL_HOST_USER
                # recipient_list=[email,]    #account@thenewshoppinghub.in
                # send_mail(subject,plain_message,email_from,recipient_list,fail_silently=False, auth_user=None, auth_password=None, connection=None,html_message=html_message)
                url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"
                print(random_str)
                payload = {"personalizations": [{"to": [{"email": email}],"subject": random_str}],"from": {"email": "anuj840084@gmail.com"},"content": [{"type": "text/plain","value": "Hello, World!"}]}
                payload =json.dumps(payload) 
                headers = {
                'content-type': "application/json",
                'x-rapidapi-host': "rapidprod-sendgrid-v1.p.rapidapi.com",
                'x-rapidapi-key': "7fded38e7emsh3c4fb60f3b8017cp1c084bjsn32180c499f5f"
                }

                response = requests.request("POST", url, data=payload, headers=headers)
                print("checking value of this")
                print(response.text)
            else:
                emailCheck,emailForm=True,True
        if "otp" in request.POST:
            otp=request.POST["otp"]
            if 'otp' in request.session:
                if otp==request.session['otp']:
                    return redirect("jobs:forgetPassword")
                else:
                    otpCheck,otpForm,emailForm=True,True,None
    context={
        'otpCheck':otpCheck,
        'emailCheck':emailCheck,
        'emailForm':emailForm,
        'otpForm':otpForm
    }
    return render(request,"jobPortal/userPassword.html",context)

def completeMember(request):
    return render(request,"jobPortal/completeMember.html")
def checkout(request):
    return render(request,"jobPortal/checkout.html")
def privacy(request):
    return render(request,"jobPortal/privacy.html")

def memberplanPricing(request,pk):
    details=TrainCertPlacement.objects.get(pk=pk)
    context={"value":details.price}
    return render(request,"jobPortal/checkout.html",context)
def memberplanPricingEmployer(request):
    if request.method=="POST":
        value=request.POST["value"]
        print("@@",type(value))
        value=int(value)
        print(type(value))
        if value== 99 or value== 499 or value== 999:
            context={"value":value}
            return render(request,"jobPortal/checkout.html",context)

def successUrl(request):
    if request.method=='POST':
        s=request.session["id"]
        s1=CheckoutMmeber.objects.get(id=s)
        print("this is the data of s1",s1)
        s1.paymentDone=True
        s1.save()
        url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"
        payload = {"personalizations": [{"to": [{"email": s1.email}],"subject": " gravitonweb.com sussfully payment done "}],"from": {"email": "anuj840084@gmail.com"},"content": [{"type": "text/plain","value": "Hello, World!"}]}
        payload =json.dumps(payload) 
        headers = {
            'content-type': "application/json",
            'x-rapidapi-host': "rapidprod-sendgrid-v1.p.rapidapi.com",
            'x-rapidapi-key': "7fded38e7emsh3c4fb60f3b8017cp1c084bjsn32180c499f5f"
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        return render(request,"jobPortal/successUrl.html")

def posted_jobs(request,pk):
    print(pk)
    if request.method == 'POST':
        print("Hi ")
    if request.user.is_authenticated:
        # if request.User.role == employer:
            job_list = Job.objects.filter(pk=pk) 
    print("edit",job_list)
    return render(request,'jobPortal/posted_jobs.html',
    {'job_list':job_list})

def jobtypes(request,pk):
    context={}
    context["company"]=Job.objects.all()
    CompanyList=[]
    primarykeys=[]
    for x in context["company"]:
        if x.company_name not in CompanyList:
            CompanyList.append(x.company_name)
            primarykeys.append(x.pk)
    context["company"]=Job.objects.filter(pk__in=primarykeys)
    locationList=[]
    primarykeys=[]
    context['location']=Job.objects.all()
    for x in context["location"]:
        if x.location not in locationList:
            locationList.append(x.location)
            primarykeys.append(x.pk)
    context["location"]=Job.objects.filter(pk__in=primarykeys)
    print(pk)
    context["jobs"]= Job.objects.filter(type=pk)
    for x in context['jobs']:
        print(type(x.type))
    print("@@checking ",context['jobs'])
    return render(request,'jobPortal/listing_right.html',context)

def updateJob(request):
    update=None
    pk=6
    if request.method == 'POST':
        primary=request.POST["primary"]
        JobTitle=request.POST["JobTitle"]
        typeJob=request.POST["typeJob"]
        company_name=request.POST["company_name"]
        website=request.POST["website"]
        salary=request.POST["salary"]
        opening=request.POST["opening"]
        phoneNumber=request.POST["phoneNumber"]
        description=request.POST["description"]
        update=True
    
    job_list = Job.objects.get(pk=primary)
    job_list.title=JobTitle
    job_list.type=typeJob
    job_list.company_name=company_name
    job_list.website=website
    job_list.salary=salary
    job_list.opening=opening
    job_list.phoneNumber=phoneNumber
    job_list.description=description
    job_list.save()
    job_list = Job.objects.filter(pk=job_list.pk) 
    return render(request,'jobPortal/posted_jobs.html',
    {'job_list':job_list,'update':update})

def ApplicantsApplied(request,pk):
    jobs=Job.objects.get(pk=pk)
    print(jobs.type)
    print(type(jobs.type))
    s=Applicant.objects.filter(job_id=pk)
    location=[]
    for x in s:
        s1=None
        try:
            s1=FullDetailEmploye.objects.get(employeeData=x.user)
        except:
            pass
        if s1 is not None:
            location.append(s1)
    print(location)
    if request.user.is_authenticated:
        if request.user.role=="employer":
            apps = Applicant.objects.all()
            applicant_list = Applicant.objects.filter(job_id=pk)
            print("@@applicant",applicant_list)
    if request.method=="POST":
        location=request.POST["location"]
        experence=request.POST["experence"]
        if location=="":
            id1=[]
            s=FullDetailEmploye.objects.filter(location=location)
            for x in s:
                id1.append(s.user_id)
            applicant_list= Applicant.objects.filter(user_id_in=id1)
            print(applicant_list)
        elif experence=="":
            id1=[]
            s=FullDetailEmploye.objects.filter(location=location)
            for x in s:
                id1.append(s.user_id)
            applicant_list= Applicant.objects.filter(user_id_in=id1)
            print(applicant_list)
        else:
            id1=[]
            s=FullDetailEmploye.objects.filter(location=location).filter(experienceTime=experence)
            for x in s:
                id1.append(s.user_id)
            applicant_list= Applicant.objects.filter(user_id_in=id1)
            print(applicant_list)

    return render(request,'jobPortal/people_applied.html',{'applicant_list':applicant_list,'jobs':jobs})

def statusChange(request,pk,ck):
    print("pk and ck cvalue",pk,ck)
    s=Applicant.objects.get(pk=pk)
    print("job primary key",s.job_id)
    s.status=ck
    s.save()
    return redirect("jobs:people_applied",s.job_id)
def careerAdv(request):
    return render(request,'jobPortal/careerAdv.html')

def allCourse(request):
    allCourse=TrainCertPlacement.objects.filter(Category=1)
    print("courses data ",allCourse)
    context={"allCourse":allCourse}
    return render(request,"jobPortal/allCourses.html",context)


def trainingCertificates(request,pk):
    print(pk)
    course=TrainCertPlacement.objects.get(pk=pk)
    training=TrainCertPlacement.objects.filter(Category=1).filter(title=course.title)
    print("training data ",training)
    placement=TrainCertPlacement.objects.filter(Category=2).filter(title=course.title)
    print("placement data ",placement)
    certificate=TrainCertPlacement.objects.filter(Category=3).filter(title=course.title)
    print("certificate data ",certificate)
    allresource=TrainCertPlacement.objects.filter(Category=4).filter(title=course.title)
    print("allresource data ",allresource)
    print(course)
    context={"training":training,"placement":placement,"certificate":certificate,"allresource":allresource,}
    return render(request,"jobPortal/training.html",context)

def traninPlacementDetails(request,pk):
    print(pk)
    details=TrainCertPlacement.objects.get(pk=pk)
    print("details view",details)
    context={"x":details}
    return render(request,"jobPortal/trainingDetails.html",context)
def memberplanPricingTraining(request,pk):
    pk=pk
    s=TrainCertPlacement.objects.get(pk=pk)
    context={"value":s.price}
    return render(request,"checkout.html",context)
def myjobs(request):
    context={}
    context["jobs"]=Job.objects.filter(user=request.user)
    print(context["jobs"])
    return render(request,"jobPortal/myjobs.html",context)

def RefundPolicy(request):
    return render(request,"jobPortal/RefundPolicy.html")

def viewallPrimum(request):
    return render(request,"jobPortal/viewallPrimum.html")

def featuredProfile(request):
    return render(request,"jobPortal/featuredProfile.html")
def resumeWriting(request):
    return render(request,"jobPortal/resumeWriting.html")
def careerBooster(request):
    return render(request,"jobPortal/careerBooster.html")
def profileHightligter(request):
    return render(request,"jobPortal/profileHightligter.html")
def linkdinMakeover(request):
    return render(request,"jobPortal/linkdinMakeover.html")
def mockInterview(request):
    return render(request,"jobPortal/mockInterview.html")
def faqEmp(request):
    return render(request,"jobPortal/faqEmp.html")
def supportEmp(request):
    return render(request,"jobPortal/supportEmp.html")
def supportCandidate(request):
    return render(request,"jobPortal/supportCandidate.html")
def documentEmp(request):
    if request.method=="POST":
        if 'companyIdCard' in request.POST:
            companyIdCard=request.POST['companyIdCard']
        else:
            companyIdCard=None
        if 'shopStablished' in request.POST:
            shopStablished=request.POST['shopStablished']
        else:
            shopStablished=None
        if 'udyogAAdhar' in request.POST:
            udyogAAdhar=request.POST['udyogAAdhar']
        else:
            udyogAAdhar=None
        if 'certificateOfIncorpation' in request.POST:
            certificateOfIncorpation=request.POST['certificateOfIncorpation']
        else:
            certificateOfIncorpation=None
        if 'msmacertificate' in request.POST:
            msmacertificate=request.POST['msmacertificate']
        else:
            msmacertificate=None
        if 'Tan' in request.POST:
            Tan=request.POST['Tan']
        else:
            Tan=None
        if 'Din' in request.POST:
            Din=request.POST['Din']
        else:
            Din=None
        s=DoucmentEmpMain.objects.create(user=request.user,companyIdCard=companyIdCard,shopStablished=shopStablished,udyogAAdhar=udyogAAdhar,certificateOfIncorpation=certificateOfIncorpation,msmacertificate=msmacertificate,Tan=Tan,Din=Din,verified=False)
        return redirect("jobs:employer-dashboard")

def webprint(request):
    return render(request,'dataFrom.html')

# @app.route('/ccavResponseHandler', methods=['GET', 'POST'])  
def ccavResponseHandler(request):
    plainText = res(request.POST['encResp'])	
    return plainText
# @app.route('/ccavRequestHandler', methods=['GET', 'POST'])
def ccavRequestHandler(request):
    p_merchant_id = request.POST['merchant_id']
    p_order_id = request.POST['order_id']
    p_currency = request.POST['currency']
    p_amount = request.POST['amount']
    p_redirect_url = request.POST['redirect_url']
    p_cancel_url = request.POST['cancel_url']
    p_language = request.POST['language']
    p_billing_name = request.POST['billing_name']
    p_billing_address = request.POST['billing_address']
    p_billing_city = request.POST['billing_city']
    p_billing_state = request.POST['billing_state']
    p_billing_zip = request.POST['billing_zip']
    p_billing_country = request.POST['billing_country']
    p_billing_tel = request.POST['billing_tel']
    p_billing_email = request.POST['billing_email']
    p_delivery_name = request.POST['delivery_name']
    p_delivery_address = request.POST['delivery_address']
    p_delivery_city = request.POST['delivery_city']
    p_delivery_state = request.POST['delivery_state']
    p_delivery_zip = request.POST['delivery_zip']
    p_delivery_country = request.POST['delivery_country']
    p_delivery_tel = request.POST['delivery_tel']
    p_merchant_param1 = request.POST['merchant_param1']
    p_merchant_param2 = request.POST['merchant_param2']
    p_merchant_param3 = request.POST['merchant_param3']
    p_merchant_param4 = request.POST['merchant_param4']
    p_merchant_param5 = request.POST['merchant_param5']
    p_integration_type = request.POST['integration_type']
    p_promo_code = request.POST['promo_code']
    p_customer_identifier = request.POST['customer_identifier']
    print("checking @@@@")
    print(p_merchant_id)
    merchant_data='merchant_id='+p_merchant_id+'&'+'order_id='+p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount+'&'+'redirect_url='+p_redirect_url+'&'+'cancel_url='+p_cancel_url+'&'+'language='+p_language+'&'+'billing_name='+p_billing_name+'&'+'billing_address='+p_billing_address+'&'+'billing_city='+p_billing_city+'&'+'billing_state='+p_billing_state+'&'+'billing_zip='+p_billing_zip+'&'+'billing_country='+p_billing_country+'&'+'billing_tel='+p_billing_tel+'&'+'billing_email='+p_billing_email+'&'+'delivery_name='+p_delivery_name+'&'+'delivery_address='+p_delivery_address+'&'+'delivery_city='+p_delivery_city+'&'+'delivery_state='+p_delivery_state+'&'+'delivery_zip='+p_delivery_zip+'&'+'delivery_country='+p_delivery_country+'&'+'delivery_tel='+p_delivery_tel+'&'+'merchant_param1='+p_merchant_param1+'&'+'merchant_param2='+p_merchant_param2+'&'+'merchant_param3='+p_merchant_param3+'&'+'merchant_param4='+p_merchant_param4+'&'+'merchant_param5='+p_merchant_param5+'&'+'integration_type='+p_integration_type+'&'+'promo_code='+p_promo_code+'&'+'customer_identifier='+p_customer_identifier+'&'
    encryption = encrypt(merchant_data,workingKey)
    mid=p_merchant_id
    encReq=encryption
    xscode=accessCode
    context={}
    context["value"]="https://test.ccavenue.cdfdfom/transaction/transaction.do?command=initiateTransaction&merchant_id="+mid+"&encRequest="+encReq+"&access_code="+xscode
    print(context["value"])		
    return render(request,"authtokenPayment.html",context)	

#Host Server and Port Number should be configured here.