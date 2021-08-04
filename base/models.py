from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserAccount(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location= models.CharField(max_length=90)
    short_intro = models.TextField()
    bio = models.TextField()
    prof_img= models.ImageField(upload_to="images")
    social_links_git = models.CharField(max_length=200)
    skills= models.CharField(max_length=500 )
     

    def __str__(self) :
        return self.name 

class Project(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    
    project_title = models.CharField(max_length=500)
    project_desc = models.TextField()
    project_img = models.ImageField(upload_to="images")
    project_link = models.CharField(max_length=1000)
    
    def __str__(self) :
        return self.user.username

 