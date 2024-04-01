from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from jobsapp.views import *
from jobsapp.views import EditProfileView, EmployerProfileEditView

from .views import *

app_name = "accounts"

urlpatterns = [
    path("employee/register/", RegisterEmployeeView.as_view(), name="employee-register"),
    path("employer/register/", RegisterEmployerView.as_view(), name="employer-register"),
    path( "employee/profile/update/", EditProfileView.as_view(), name="employee-profile-update", ),
    # path(  "employer/profile/updates/",  EmployerProfileEditView.as_view(),  name="employer-profile-update", ),
    path("logout/", LogoutView.as_view(), name="logout"),
     path( "employer/profile/updatde/",  EmployerProfileEdit,  name="employer-profile-update", ),
    path("login/", LoginView.as_view(), name="login"),
    # path("/account/login/", LoginView1.as_view(), name="Accountlogin"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
