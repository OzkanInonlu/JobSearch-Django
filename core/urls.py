from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "core"

urlpatterns = [
    path("", views.home_page, name = "home_page"),
    path('accounts/login/', views.login_user, name = "login"),
    path('logout/', views.logout_user, name = "logout"),
    path('accounts/register-applicant/', views.register_applicant, name = "register_applicant"),
    path('accounts/register-employer/', views.register_employer, name = "register_employer"),
    # path('proxy/', views.proxy, name = "proxy"),
    path('about-us/', views.about_us, name = "about_us"),
    path('dashboard/applicant-dashboard/', views.applicant_dashboard, name = "applicant_dashboard"),
    path('dashboard/employer-dashboard/', views.employer_dashboard, name = "employer_dashboard"),
    #path("", views.home_dashboard, name = "home_dashboard"),
    path("update-company/", views.update_company, name = "update_company"),
    path("company-details/<int:id>", views.company_details, name = "company_details"),
    path("applicant/update-resume/", views.update_resume, name = "update_resume"),
    path("applicant/resume-details/<int:id>", views.resume_details, name = "resume_details"),

    path("applicant/my-profile/<int:id>", views.my_profile, name = "my_profile"),
    path("all-available-applicants/", views.all_available_applicants, name = "all_available_applicants"),
    
    path("job-adverts/create-job-advert/", views.create_job_advert, name = "create_job_advert"),
    path("job-adverts/update-job-advert/<int:id>", views.update_job_advert, name = "update_job_advert"),
    path("job-adverts/all-job-adverts", views.all_job_adverts, name = "all_job_adverts"),
    path("job-adverts/job-advert/<int:id>", views.single_job_advert, name = "single_job_advert"),
    path("job-adverts/manage-job-adverts", views.manage_job_adverts, name = "manage_job_adverts"),
    path("job-adverts/apply-to-job/<int:id>", views.apply_to_job, name = "apply_to_job"),
    path("job-adverts/<int:id>/all-applicants/", views.all_applicants, name = "all_applicants"),
    path("job-adverts/delete-job-adverts/<int:id>", views.delete_job_advert, name = "delete_job_advert"),
    path("all-applicants/applicant/<int:id>", views.single_applicant_detail, name = "single_applicant_detail"),
    path("applicant/all-applied-jobs", views.applied_jobs, name = "applied_jobs"),
    path("applicant/delete-application/<int:id>", views.delete_application, name = "delete_application"),
    path("send-user-recovery-sms", views.send_user_recovery_sms, name = "send_user_recovery_sms"),
    path("send-user-recovery-email", views.send_user_recovery_email, name = "send_user_recovery_email"),
    path("make-comment/",views.make_comment,name="make_comment"),
    path("change_application_status/<int:id>",views.change_application_status, name="change_application_status")


    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
