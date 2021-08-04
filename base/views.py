from django.http import HttpResponse
from django import views
from django.shortcuts import render,redirect
from django.http import HttpResponse, request
from django.views import View 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from . models import *
# Create your views here.
 

class DevContact(View):
    def get(self, request,id):
        return render(request,'devcontact.html',{'user_id':id})
    def post(self,request,id):
        subject = request.POST.get('name')
        message= request.POST.get('message')
        user_id = request.POST.get('user_id')
        mail_sender = request.POST.get('email')
        email_from = mail_sender
        print(mail_sender)
        try:
            dev_mail  = UserAccount.objects.filter(id = user_id).first()
            send_mail(subject, message, email_from, [dev_mail.user.email], fail_silently=False) 
            messages.success(request,"Message has been sent sucessfully") 
            return render(request,"devcontact.html")
        except BadHeaderError:  
            return HttpResponse("Invalid sent")


class Index(View):
    def get(self,request):
        items = UserAccount.objects.all()
        return render(request, 'index.html',{'items':items} )

class DevSearch(View):
    def get(self,request ):
        queryset = request.GET.get('queryset') 
        allpostTitle = UserAccount.objects.filter(name__icontains=queryset) 
        allpostDesc = UserAccount.objects.filter(skills__icontains=queryset) 
         
        allpost= allpostTitle.union(allpostDesc) 
         
        return render(request,'devsearch.html',{'items':allpost,'query':queryset} )

class HandleSignup(View):
    def get(self,request):
        return render(request,'index.html')
    def post(self,request):
        username= request.POST.get('username')
        email= request.POST.get('email')
        pass1= request.POST.get('pass1')
        pass2= request.POST.get('pass2')  
        cust = User.objects.filter(email=email).first()
        cust1 = User.objects.filter(username=username).first()   
        if cust or cust1:
            messages.error(request,"Details already found")
            return redirect('index')

        if pass1 != pass2:
            messages.error(request,"Your password does'nt match")
            return redirect('index')
        myuser = User.objects.create_user(username,email,pass1)   
        myuser.save() 
        messages.success(request,"Your account has been created sucessfully")
        return redirect('index')


class HandleLogin(View):
    def get(self,request):
        return render(request,'index.html')
    def post(self,request):
        username = request.POST.get('username')   
        pass1 = request.POST.get('pass1')
        user = authenticate(username=username,password=pass1)
        if user is not None:
            login(request,user)
            messages.success(request,"Your Login sucessfully")
            return redirect('index')
        else:
            messages.error(request,"Invalid Details")
            return redirect('index')


class HandleLogout(View):
    def get(self,request):
        logout(request)
        messages.success(request,"Your Logout sucessfully")
        return redirect('index')  
def send_forget_password_mail(email,user ):
         
        subject = 'Your forget password link'
        message = f'Hi, Click the link to reset your password http://127.0.0.1:8000/change_pass/{user.id}' 
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)
        return True    
class ForgetPassword(View):
    def get(self, request):
        return render(request,'forget_pass.html')
    def post(self, request):
        email=request.POST.get('email')
        if not User.objects.filter(email=email ).first():
            messages.error(request,"Invalid E-Mail")
            return redirect('forget_pass')
        else: 
             
            user_obj = User.objects.get(email=email) 
             
            user_id =User.objects.get(id=user_obj.id) 
            
            send_forget_password_mail(user_obj.email, user_id )
            messages.success(request,"We have sent an e-mail to your given email")
            return redirect( 'forget_pass')
    

class ChangePassword(View):
    def get(self,request,id):
        # user_id = User.objects.filter(id=id).first()
        return render(request,'change_pass.html',{'user_id':id})
    def post(self,request,id ):
        user_obj = User.objects.filter(id=id).first()
        context = {'user_id':user_obj}
        newpass = request.POST.get('newpass')
        newpass1 = request.POST.get('newpass1')
        user_id = request.POST.get('user_id')
        if user_id is None:
            messages.error(request,"User Not FOUND")
            return redirect( f'http://127.0.0.1:8000/change_pass/{user_id}')
        if newpass != newpass1:
            messages.error(request,"Password doesnt match")
            return redirect( f'http://127.0.0.1:8000/change_pass/{user_id}')
        user_obj = User.objects.get(id=user_id)  
        user_obj.set_password(newpass) 
        user_obj.save()
        messages.success(request,"Your password has been changed, Now you can login ")
        return redirect('index')


    


class AddDetails(View):
    def get(self,request) :
        return render(request,'adddetails.html')  

    def post(self,request):
        name=request.POST.get('name')   
        email=request.POST.get('email')
        location = request.POST.get('location')
        short_intro = request.POST.get('short_intro') 
        bio = request.POST.get('bio')   
        social_links_git= request.POST.get('social_links_git')    
        prof_img = request.FILES.get('prof_img')
        skills = request.POST.get('skills')
        user = request.POST.get('user_id')
        user = request.user
        if user is not None:
            myaccount = UserAccount(name=name,skills=skills, email=email,location=location,short_intro = short_intro, bio=bio,prof_img=prof_img,social_links_git=social_links_git,user=user)
            messages.success(request,"You sucessfully added your details") 
            myaccount.save()
            return redirect('adddetails')

class MyAccount(View):
    def get(self, request  ):
        if request.user.is_authenticated:
            user = request.user
            myproj = Project.objects.filter(user=user) 
            item =UserAccount.objects.filter(user=user).first()
            return render(request,'account.html',{'item':item,'myproj':myproj})   
class MyAllProjects(View):
    def get(self, request,id):
        myallproj = Project.objects.filter(id=id).first()
        return render(request,'myallprojects.html',{'item':myallproj})      
class DevDetails(View):
    def get(self,request,id):
         
        devdet = UserAccount.objects.filter(id=id).first()
          
        return render(request,'developerdetail.html', {'item':devdet })               
 
class MyProject(View):
    def get(self,request):
        return render(request,'addproject.html')     
    def post(self,request):
        user = request.POST.get('user_id')
        
        project_title =request.POST.get('project_title')
        project_desc =request.POST.get('project_desc')
        project_link =request.POST.get('project_link')
        project_img =request.FILES.get('project_img')
        user = request.user
        if user is not None:
            pro = Project(user=user,  project_desc=project_desc,project_img=project_img,project_link=project_link,project_title=project_title)
            messages.success(request,"You sucessfully added your project")
            pro.save()
            return redirect('addproject')
        if not user==request.user  :
            return HttpResponse("404 Not Found")  

class AllProjects(View):
    def get(self,request):
        items = Project.objects.all().order_by("-id")
        return render(request,'projects.html',{'items':items})

class EditDetails(View):
    def get(self, request,id ):
        return render(request,'editdetail.html',{'account_id':id}  )
         
    def post(self, request,id):
        name=request.POST.get('name')   
        email=request.POST.get('email')
        location = request.POST.get('location')
        short_intro = request.POST.get('short_intro') 
        bio = request.POST.get('bio')   
        social_links_git= request.POST.get('social_links_git')    
        prof_img = request.FILES.get('prof_img')
        skills = request.POST.get('skills')
        account_id = request.POST.get('account_id')
         
      
        myaccount = UserAccount.objects.get(id=account_id) 
        myaccount.name=name
        myaccount.email=email
        myaccount.location=location
        myaccount.short_intro=short_intro
        myaccount.bio=bio
        myaccount.social_links_git=social_links_git
        myaccount.prof_img=prof_img
        myaccount.skills = skills
        messages.success(request,"Your details are updated")
        myaccount.save()
        return redirect("account")


class Search(View):
    def get(self,request ):
         
         
        query = request.GET.get('query') 
        allpostTitle = Project.objects.filter(project_title__icontains=query) 
        allpostDesc = Project.objects.filter(project_desc__icontains=query) 
         
        allpost= allpostTitle.union(allpostDesc) 
         
        return render(request,'projsearch.html',{'items':allpost,'query':query} )


 