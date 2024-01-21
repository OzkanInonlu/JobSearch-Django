from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required 
from .filter import *
import smtplib
from email.mime.multipart import MIMEMultipart   # mail yapısını olusturacak bu sınıf
from email.mime.text import MIMEText           # mesaj olusturmak icin bu sınıfı kullanacaz
from twilio.rest import Client



User = get_user_model()

#register applicants

def register_applicant(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST or None)


        if form.is_valid():
            var = form.save(commit=False)
            var.is_applicant=True
            var.username = var.email
            var.save()

            #Resume.objects.create(user=var)
            
            messages.success(request, "Successfully registered.")    

            subject = "JobSearchApp Welcome Message" #mailin konusu yani başlığı

            message = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Welcome to Our Platform</title>
                        <style>
                            body {
                                font-family: Arial, sans-serif;
                                background-color: #f4f4f4;
                                color: #333;
                                margin: 0;
                                padding: 0;
                            }

                            .container {
                                width: 80%;
                                max-width: 600px;
                                margin: 50px auto;
                                background-color: #fff;
                                padding: 20px;
                                border-radius: 8px;
                                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                            }

                            h2 {
                                color: #007BFF;
                            }

                            p {
                                margin-bottom: 20px;
                                font-size: 16px;

                            }

                            .button {
                                display: inline-block;
                                padding: 10px 20px;
                                font-size: 16px;
                                text-align: center;
                                text-decoration: none;
                                background-color: #647490;
                                color: white !important;
                                border-radius: 4px;
                            }

                            .button:hover {
                                background-color: #0056b3;
                            }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h2>Welcome to Our Platform!</h2>
                            <p>We are thrilled to have you on board. Explore our platform and discover amazing opportunities.</p>
                            <p>To get started, click the button below:</p>
                            <a class="button" href="http://127.0.0.1:8000/accounts/login/">Go to Dashboard</a>
                            <p>If you have any questions or need assistance, feel free to reach out to our support team.</p>
                            <p>Thank you for joining us,<br>Job Search App</p>
                        </div>
                    </body>
                    </html>
                    """
            try:
                send_user_email(var.username, subject, message)
                messages.success(request, ("Confirmation email has been sent to your account."))
                return redirect("core:login")

            except Exception as e:
                messages.warning(request, ("An error occurred while sending email, please try again later."))
                return redirect("core:login")
          
        else:
            messages.warning(request, form.errors.as_text().split("*")[2])
            return redirect("core:register_applicant")
    else:
        form = RegisterForm()
        return render(request, "users/applicants/register_applicant.html", {"form": form})
    

#register employers
def register_employer(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            var = form.save(commit=False)
            var.is_employer=True
            var.username = var.email
            var.save()

            #Company.objects.create(user=var)
            
            messages.success(request, "Successfully registered.") 
            subject = "JobSearchApp Welcome Message" #mailin konusu yani başlığı

            message = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Welcome to Our Platform</title>
                        <style>
                            body {
                                font-family: Arial, sans-serif;
                                background-color: #f4f4f4;
                                color: #333;
                                margin: 0;
                                padding: 0;
                            }

                            .container {
                                width: 80%;
                                max-width: 600px;
                                margin: 50px auto;
                                background-color: #fff;
                                padding: 20px;
                                border-radius: 8px;
                                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                            }

                            h2 {
                                color: #007BFF;
                            }

                            p {
                                margin-bottom: 20px;
                                font-size: 16px;

                            }

                            .button {
                                display: inline-block;
                                padding: 10px 20px;
                                font-size: 16px;
                                text-align: center;
                                text-decoration: none;
                                background-color: #647490;
                                color: white !important;
                                border-radius: 4px;
                            }

                            .button:hover {
                                background-color: #0056b3;
                            }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h2>Welcome to Our Platform!</h2>
                            <p>We are thrilled to have you on board. Explore our platform and discover amazing opportunities.</p>
                            <p>To get started, click the button below:</p>
                            <a class="button" href="http://127.0.0.1:8000/accounts/login/">Go to Dashboard</a>
                            <p>If you have any questions or need assistance, feel free to reach out to our support team.</p>
                            <p>Thank you for joining us,<br>Job Search App</p>
                        </div>
                    </body>
                    </html>
                    """
            try:
                send_user_email(var.username, subject, message)
                messages.success(request, ("Confirmation email has been sent to your account."))
                return redirect("core:login")

            except Exception as e:
                messages.warning(request, ("An error occurred while sending email, please try again later."))
                return redirect("core:login")      
        else:
            messages.warning(request, form.errors.as_text().split("*")[2])
            return redirect("core:register_employer")    

    else:
        form = RegisterForm()
        return render(request, "users/employers/register_employer.html", {"form": form})


#login user
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                if user.is_applicant:
                    return redirect('core:applicant_dashboard')
                elif user.is_employer:
                    return redirect('core:employer_dashboard')

            else:
                messages.warning(request,"Please check your credentials")
                return redirect('core:login')
    else:
        form = LoginForm()
        passwordForm = ForgotPasswordForm()
        return render(request, "users/login.html", {'form': form, "passwordForm":passwordForm})

    
#logout
def logout_user(request):
    logout(request)
    messages.success(request, "Your session has ended.")
    return redirect("core:login")

def about_us(request):
    return render(request, "website/about_us.html")
@login_required(login_url = "core:login")
def applicant_dashboard(request):
    job_adverts_list = JobAdvert.objects.all().order_by("-created_at")
    filter_query = JobAdvertFilter(request.GET, queryset=job_adverts_list)
    comment_list = Comment.objects.all()
    return render(request, "dashboard/applicant_dashboard.html", {"filter_query":filter_query, "comment_list":comment_list})
@login_required(login_url = "core:login")
def employer_dashboard(request):
    job_adverts_list = JobAdvert.objects.all().order_by("-created_at")
    filter_query = JobAdvertFilter(request.GET, queryset=job_adverts_list)
    comment_list = Comment.objects.all()
    return render(request, "dashboard/employer_dashboard.html", {"filter_query":filter_query, "comment_list":comment_list})

@login_required(login_url = "core:login")
def update_company(request):

    if request.user.is_employer:
        user = User.objects.filter(id = request.user.id).first()
        if request.method == 'POST':
            form = UpdateCompanyForm(request.POST)
            if form.is_valid():
                company_name = request.POST["company_name"]
                establishment_date = request.POST["establishment_date"]
                city_option = form.cleaned_data["city_option"]
                state = request.POST["state"]
                if city_option == "N":
                    city = "Nicosia"
                elif city_option == "K":
                    city = "Kyrenia"
                elif city_option == "F":
                    city = "Famagusta"
                elif city_option == "O":
                    city = "Omorfo"
                elif city_option == "L":
                    city = "Lefke"
                elif city_option == "S":
                    city = "South Cyprus"
                else:
                    messages.error(request, ("Invalid City Option."))
                    return redirect("core:update_company")
                if user.has_company: #update
                    if company_name and establishment_date and city and state:
                        Company.objects.filter(user = request.user).update(company_name = company_name, establishment_date = establishment_date, city = city, state = state)
                        messages.success(request, "Your company has been updated")
                        return redirect("core:employer_dashboard")
                
                else: #no company
                    Company.objects.create(
                        user = user, company_name = company_name, 
                        establishment_date = establishment_date, city = city, 
                        state = state)
                    user.has_company = True
                    user.save()
                    messages.success(request, "Your company has been updated")
                    return redirect("core:employer_dashboard")
        else: #get
            form = UpdateCompanyForm()
            company = Company.objects.filter(user = request.user).first()
            return render(request, "users/employers/update_company.html", {"company":company, "form":form})

    else:
        messages.error(request, "Permission denied")
        return redirect('core:employer_dashboard')
    


def company_details(request, id):

    company = Company.objects.filter(id = id).first()

    return render(request, 'website/company_details.html',{"company":company})

# def is_valid_file(file): #to accept only PDF or Word files
#     mime = magic.Magic()
#     file_type = mime.from_buffer(file.read(1024))  # Read the first 1024 bytes to determine file type
#     return file_type.startswith('application/pdf') or file_type.startswith('application/msword')

@login_required(login_url = "core:login")
def update_resume(request):
    #check if that user has a resume or not??? 
    if request.user.is_applicant:
        user = User.objects.filter(id = request.user.id).first()
        if request.method == 'POST':
            form = UpdateResumeForm(request.POST, request.FILES)
            if form.is_valid():
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                nationality = form.cleaned_data["nationality"]
                job_title = form.cleaned_data["job_title"]
                resume_file = request.FILES.get('resume_file')

                # if not is_valid_file(resume_file.file):
                #     messages.warning(request, "Invalid file type. Please upload a PDF or Word document.")
                #     return redirect("core:update_resume")
    
                if user.has_resume: #update
                    resume=Resume.objects.filter(user = request.user).first()
                    if first_name and last_name and nationality and job_title:
                        if resume_file:
                            with open('media/' + resume_file.name, 'wb+') as file:
                                for chunk in resume_file.chunks():
                                    file.write(chunk)

                            resume.upload_resume=resume_file

                        resume.first_name = first_name
                        resume.last_name = last_name
                        resume.nationality = nationality
                        resume.job_title = job_title
                        resume.save()
                        
                        messages.success(request, "Your resume has been updated")
                        return redirect("core:applicant_dashboard")
                    
                    else:
                        messages.warning(request, "Please fill all inputs")
                        return redirect("core:update_resume")
                
                else: #no resume
                    Resume.objects.create(
                        user = user, first_name = first_name, 
                        last_name = last_name, nationality = nationality, 
                        job_title = job_title, 
                        upload_resume = resume_file)
                    user.has_resume = True
                    user.save()
                    messages.success(request, "Your resume has been created")
                    return redirect("core:applicant_dashboard")
        else: #get
            resume = Resume.objects.filter(user = request.user).first()

            if resume:

                form = UpdateResumeForm(initial={
                    'first_name': resume.first_name,
                    'last_name': resume.last_name,
                    'nationality': resume.nationality,
                    'job_title': resume.job_title,
                })
                
                #check if resume file is uploaded?
                if resume.upload_resume:
                    has_resume_file=True
                else:
                    has_resume_file=False

                return render(request, "users/applicants/update_resume.html", {"resume":resume, "form":form, "has_resume_file":has_resume_file})

            else:
                form = UpdateResumeForm()
                return render(request, "users/applicants/update_resume.html", {"resume":resume, "form":form})
    else:
        messages.error(request, "Permission denied")
        return redirect('core:applicant_dashboard')
@login_required(login_url = "core:login")
def resume_details(request, id):
    resume = Resume.objects.filter(id = id).first()
    return render(request, 'users/applicants/resume_details', {"resume":resume})

@login_required(login_url = "core:login")
def create_job_advert(request):
    if request.user.is_employer and request.user.has_company:

        #industries
        INDUSTRIES = list(Industry.objects.values_list('name', flat=True))

        form = CreateJobAdvertForm(request.POST or None)
        if form.is_valid():
            industry = Industry.objects.filter(name = request.POST["industry"]).first()
            if (float(form.cleaned_data["min_salary"]) > float(form.cleaned_data["max_salary"]) ) or (float(form.cleaned_data["max_salary"]) ==0):
                messages.warning(request, "Please adjust the salaries properly.")
            else:
                job_advert = JobAdvert.objects.create(
                    user = request.user,
                    company = request.user.company,
                    title = form.cleaned_data['title'],
                    location = form.cleaned_data['location'],
                    max_salary = form.cleaned_data['max_salary'],
                    min_salary = form.cleaned_data['min_salary'],
                    description = form.cleaned_data['description'],
                    is_available = form.cleaned_data['is_available'],
                    job_type = form.cleaned_data['job_type'],
                    industry=industry
                )

                messages.success(request, "Job advert has been created")
                return redirect('core:employer_dashboard')

        return render(request, "users/employers/create_job_advert.html", {'form': form, "INDUSTRIES":INDUSTRIES})
    else:
        messages.error(request, "Permission denied")
        return redirect('core:employer_dashboard')
    
@login_required(login_url = "core:login")
def update_job_advert(request, id):
    job_advert = JobAdvert.objects.filter(id=id).first()
    INDUSTRIES = list(Industry.objects.values_list('name', flat=True))

    if request.method == 'POST':

        title = request.POST.get('title')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        max_salary = request.POST.get('max_salary')
        min_salary = request.POST.get('min_salary')
        description = request.POST.get('description')
        is_available = request.POST.get('is_available') #on or off
        industry = Industry.objects.filter(name = request.POST.get("industry")).first()

        if title and location and max_salary and min_salary and description and industry:
            JobAdvert.objects.filter(id=id).update(title=title, location=location,
                     max_salary=max_salary, min_salary=min_salary,
                     job_type=job_type, description=description,
                     industry=industry)
            
            if is_available is not None:
                JobAdvert.objects.filter(id=id).update(is_available=True)
            else:
                JobAdvert.objects.filter(id=id).update(is_available=False)

            messages.success(request, "Job advert has been updated")
            return redirect('core:manage_job_adverts')
        else:
            messages.warning(request, "Something went wrong, please try again")
            return redirect('core:update_job_advert')
    return render(request, "users/employers/update_job_advert.html", {"job_advert":job_advert, "INDUSTRIES":INDUSTRIES})


#normal landing page
def home_page(request):
    job_adverts_list = JobAdvert.objects.all().order_by("-created_at")
    filter_query = JobAdvertFilter(request.GET, queryset=job_adverts_list)
    comment_list = Comment.objects.all()
    return render(request, "website/home_page.html", {"filter_query":filter_query, "comment_list":comment_list})



#all available job adverts
def all_job_adverts(request):
    job_adverts_list = JobAdvert.objects.filter(is_available=True).order_by("-created_at")
    filter_query = JobAdvertFilter(request.GET, queryset=job_adverts_list)
    return render(request, "website/all_job_adverts.html", {"filter_query":filter_query})


#detail of a job advert
def single_job_advert(request, id):
    job_advert = JobAdvert.objects.get(id=id)
    all_job_adverts_of_company = JobAdvert.objects.filter(company=job_advert.company)
    return render(request, "website/single_job_advert.html",
                   {"job_advert":job_advert, 
                    "all_job_adverts_of_company":all_job_adverts_of_company})


#managing job adverts by employer
@login_required(login_url = "core:login")
def manage_job_adverts(request):
    all_job_adverts = JobAdvert.objects.filter(user = request.user, company=request.user.company).order_by("-created_at")
    return render(request, "users/employers/manage_job_adverts.html", {"all_job_adverts":all_job_adverts})

@login_required(login_url = "core:login")
def apply_to_job(request, id):
    
    if request.user.is_applicant:

        if request.user.has_resume:

            job = JobAdvert.objects.get(id=id)

            #check if user applied to this job before
            if ApplyJob.objects.filter(user = request.user, job=job).first():
                messages.warning(request, "You've already applied to that job")
                return redirect("core:single_job_advert", id=id)
            else:
                ApplyJob.objects.create(user = request.user, job=job, status="P")
                messages.success(request, "Successfully applied to job")
                return redirect("core:single_job_advert", id=id)
        
        else:
            messages.warning(request, "Please first set your resume.")
            return redirect("core:update_resume")

    else:
        messages.error(request, "Permission denied. Only applicants can apply.")
        return redirect("core:single_job_advert", id=id)


#to see the applicants applied to the job
@login_required(login_url = "core:login")
def all_applicants(request, id):
    job = JobAdvert.objects.get(id=id)

    #ApplyJob object
    applicants = job.applyjob_set.all().order_by("applied_at")

    return render(request, "users/employers/all_applicants.html", {"job":job, "applicants":applicants})

#to accept/reject applicant
@login_required(login_url = "core:login")
def change_application_status(request, id):
    if request.user.is_employer:
        application=ApplyJob.objects.get(id=id)
        # if application.status == "A":
        #     application.status = 'R'
        #     application.save()
        # elif application.status == "R" or application.status =="P":
        #     application.status = "A"
        #     application.save()
        # messages.success(request, "Applicant status changed")
        # return redirect("core:manage_job_adverts")
        if request.method == "POST":
            action=request.POST.get("action")
            if action=="accept":
                application.status="A"
                application.save()
            elif action=="reject":
                application.status="R"
                application.save()
            else:
                messages.error(request,"Invalid Action")
            return redirect("core:manage_job_adverts")

    else:
        messages.error(request, "Permission denied. Only employers can perform this action.")
        return redirect("core:manage_job_adverts")



#list all jobseekers available on the website
def all_available_applicants(request):
    applicants=User.objects.filter(is_applicant=True)
    if applicants:
        return render(request, "users/employers/all_available_applicants.html", {"applicants":applicants})
    else:
        messages.warning(request, "No available applicants")
        return redirect("core:employer_dashboard")

#to see an applicant profile 
def single_applicant_detail(request, id):

    applicant = User.objects.filter(is_applicant = True, id=id).first()
   
    return render(request, "website/single_applicant_detail.html", {"applicant":applicant})

@login_required(login_url = "core:login")
#to see the applicants's applied jobs
def applied_jobs(request):
    applied_jobs = ApplyJob.objects.filter(user=request.user).order_by("-applied_at")
    return render(request, "users/applicants/applied_job_adverts.html", {"applied_jobs":applied_jobs})

#delete job application
@login_required(login_url = "core:login")
def delete_application(request, id):
    application = ApplyJob.objects.filter(user = request.user, id=id).first()
    if application:
        if application.status == "A":
            messages.warning(request, "You have been accepted for that job, cannot delete it.")
            return redirect("core:applied_jobs")
        else:
            application.delete()
            messages.info(request, "Your application has been deleted")
            return redirect("core:applied_jobs")
    else:
        messages.error(request, "No application found")
        return redirect("core:applied_jobs")

#applicant profile    
@login_required(login_url = "core:login")
def my_profile(request, id):
    applicant = User.objects.filter(is_applicant = True, id=id).first()
    if request.method == "POST":
        form=EmailChangingForm(request.POST)
        if form.is_valid():
            new_email=form.cleaned_data["email"]
            applicant.email=new_email
            applicant.username=new_email
            applicant.save()
            messages.success(request, "Email has been updated.")
        else:
            messages.warning(request, "Something went wrong. Please try again.")
    else:
        form=EmailChangingForm(initial={"email":applicant.email})
    return render(request, "users/applicants/my_profile.html", {"applicant":applicant, "form":form})

    
@login_required(login_url = "core:login")
def delete_job_advert(request, id):
    job_advert = JobAdvert.objects.filter(user = request.user, id=id).first()
    if job_advert:
        job_advert.delete()
        messages.info(request, "Job advertisement has been deleted")
        return redirect("core:manage_job_adverts")
    else:
        messages.error(request, "No advertisement found")
        return redirect("core:manage_job_adverts")


#email sending function
def send_user_email(send_to, subject, message):
    email=MIMEMultipart()
    email["From"] = "highgamers01@gmail.com"  #kimden gidecek?
    email["To"] = send_to
    email["Subject"] = subject #mailin konusu yani başlığı
    #mail yapısını olusturduk

    #mail içinde ne yazacak?

    email_body=MIMEText(message,"html") #plain text dedik yani normal bir text oldugu için

    email.attach(email_body) #mail yapısına gönderdik mesajı
    try:
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.ehlo() # kendimizi bagladık
        server.starttls()
        server.login("highgamers01@gmail.com","rwtpmwrbuhrhhmyf")
        server.sendmail(email["From"],email["To"],str(email)) #multipart yapısından str'e dönüstürdük mesajı --> mesaj.as_string()
        server.quit()
        
    except Exception as e:
        return redirect("core:login")



    
def send_user_recovery_email(request):
    
    form = ForgotPasswordForm(request.POST or None)
    if form.is_valid():

        subject = "JobSearchApp Password Recovery" #mailin konusu yani başlığı
        
        module_dir = os.path.dirname(__file__)  
        file_path = os.path.join(module_dir, 'common-passwords.txt')   #full path to text.
        with open(file_path,"r") as f:
            lst=[]
            for p in f.readlines():
                p = p.strip()
                lst.append(p)
        new_password = random.choice(lst)
        #mail içinde ne yazacak?

        # message = f"""
        # JobSearchApp - Password Recovery Email. 
        # You requested a new password. 
        # Your new password: " {new_password} "
        # """

        message = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Password Recovery</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            color: #333;
                            margin: 0;
                            padding: 0;
                        }

                        .container {
                            width: 80%;
                            max-width: 600px;
                            margin: 50px auto;
                            background-color: #fff;
                            padding: 20px;
                            border-radius: 8px;
                            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                        }

                        h2 {
                            color: #007BFF;
                        }

                        p {
                            margin-bottom: 20px;
                            font-size: 16px;

                        }

                        .button {
                            display: inline-block;
                            padding: 10px 20px;
                            font-size: 16px;
                            text-align: center;
                            text-decoration: none;
                            background-color: #647490;
                            color: white !important;
                            border-radius: 4px;
                        }

                        .button:hover {
                            background-color: #0056b3;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2>Password Recovery</h2>
                        <p>We received a request to reset your password. If you did not make this request, please ignore this email.</p>
                        <p>To reset your password, click the button below:</p>
                        <a class="button" href="http://127.0.0.1:8000/accounts/login/">Reset Password</a>
                        <p>If the button above doesn't work, you can also copy and paste the following link into your browser:</p>
                        <p>http://127.0.0.1:8000/accounts/login/</p>
                        <p>This link will expire in 1 hour for security reasons.</p>
                        <p>If you have any questions or concerns, please contact our support team.</p>
                        <p>Thank you,<br>Job Search App</p>
                    </div>
                </body>
                </html>
                """

        try:
            send_user_email(form.cleaned_data["user_email"], subject, message)
            messages.success(request, ("Password Recovery email has been sent to your account."))
            return redirect("core:login")

        except Exception as e:
            messages.warning(request, ("An error occurred while sending email, please try again later."))
            return redirect("core:login")
    else:
        messages.warning(request, ("Wrong email format, please try again."))
        return redirect("core:login")

#sms sending function
def send_user_sms(request,send_to, message_body):
    try:
        account_sid = settings.ACCOUNT_SID
        auth_token = settings.AUTH_TOKEN
        client = Client(account_sid, auth_token)
        message = client.messages.create(
                                body=f'Your new password is " {message_body} " ',
                                from_='+14782922395',
                                to=send_to)
        messages.success(request, ("SMS succesfully has been sent to your phone."))

    except Exception as e:
        messages.warning(request, ("An error occurred while sending SMS, please try again later.") + str(e))



def send_user_recovery_sms(request):
    form = ForgotPasswordForm(request.POST or None)
    if form.is_valid():
        try:
            module_dir = os.path.dirname(__file__)  
            file_path = os.path.join(module_dir, 'common-passwords.txt')   #full path to text.
            with open(file_path,"r") as f:
                lst=[]
                for p in f.readlines():
                    p = p.strip()
                    lst.append(p)
            new_password = random.choice(lst)
            send_user_sms(request, form.cleaned_data["user_phone_no"], new_password)
            return redirect("core:login")
        except Exception as e:
            return redirect("core:login")

    else:
        messages.warning(request, ("Wrong phone number format, please try again."))
        return redirect("core:login")

@login_required(login_url = "core:login")
def make_comment(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            email = request.POST.get("email")
            comment = request.POST.get("comment")
            if email and comment:
                Comment.objects.create(user=request.user, email=email, comment=comment)
                messages.success(request, ("We got your feedback. Thanks in advance."))
                return redirect("core:about_us")
            else:
                messages.warning(request, ("Please fill in the required informations."))
                return redirect("core:about_us")
    else:
        messages.info(request, ("In order to make a comment, first sign in or sign up."))
        return redirect("core:about_us")