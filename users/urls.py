from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "users"

urlpatterns = [
    path('login/', views.login_user, name = "login"),
    path('logout/', views.logout_user, name = "logout"),
    path('register-applicant/', views.register_applicant, name = "register_applicant"),
    path('register-employer/', views.register_employer, name = "register_employer"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
