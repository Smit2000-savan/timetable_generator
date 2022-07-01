# """sri URL Configuration
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/3.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add coordinator URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add coordinator URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add coordinator URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path, include
# from .views import home
# from . import views
# from django.views.generic.base import TemplateView # new
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', home.as_view(), name='Home'),
#     # path('logout_user', views.logout_user, name='logout_user'),
#
#     # path("accounts/", include("django.contrib.auth.urls")),  # new
#     # path('', TemplateView.as_view(template_name='home.html'), name='home'),  # new
#
#     path('professor/', include('professor.urls')),
#     path('accounts/', include('allauth.urls')),
#
# ]

"""sri URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add coordinator URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add coordinator URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add coordinator URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView # new

urlpatterns = [
    # path('admin', admin.site.urls),

    # HOMEPAGE ----

    path('', views.home,name='Home'),

    # PROFESSOR ----

    path('p_login_user', views.p_login, name='plogin'),
    path('p_login_user/p_preferences', views.p_index, name="pindex"),
    # path('p_pref/<str:u>',views.index,name="p_pref"),

    # CO-ORDINATOR ----

    path('c_login_user', views.c_login, name="clogin"),
    path('c_index', views.c_index, name='cindex'),

    path('c_courses', views.c_course, name='ccourse'),
    path('c_addCourse', views.c_addCourse, name='addCourse'),
    path('c_courseRecord', views.c_courseRecord, name='courseRecord'),
    path('c_deleteCourse/<int:id>', views.c_deleteCourse, name='deleteCourse'),

    path('c_batches', views.c_batch, name='cbatch'),
    path('c_addBatch', views.c_addBatch, name='addBatch'),
    path('c_batchRecord', views.c_bacthRecord, name='batchRecord'),
    path('c_deleteBatch/<int:id>', views.c_deleteBatch, name='deleteBatch'),

    path('c_faculty', views.c_facultyDetails, name='cfacultyDetails'),
    path('c_addFaculty', views.c_addFaculty, name='addFaculty'),
    path('c_facultyRecord', views.c_facultyRecord, name='facultyRecord'),
    path('c_deleteFaculty/<int:id>', views.c_deleteFaculty, name='deleteFaculty'),

    # COMMON / TEMP ----

    path('logout_user', views.logout_user, name='logout_user'),
    path('Timetable', views.Timetable, name="Timetable"),
]
