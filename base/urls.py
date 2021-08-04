 
from django.urls import path
from . import views

urlpatterns = [
    path('',views.Index.as_view(), name="index" ),
     
    path('developerdetail/<int:id>/',views.DevDetails.as_view(), name="developerdetail" ),
    path('developerdetail/devcontact/<int:id>/',views.DevContact.as_view(), name="devcontact" ),
     
    path('handlesignup',views.HandleSignup.as_view(), name="handlesignup"),
    path('handlelogin',views.HandleLogin.as_view(), name="handlelogin"),
    path('handlelogout',views.HandleLogout.as_view(), name="handlelogout"), 
    path('forget_pass/', views.ForgetPassword.as_view(),name="forget_pass"),
    path('change_pass/<int:id>/', views.ChangePassword.as_view(),name="change_pass"),
    path('adddetails/', views.AddDetails.as_view(), name="adddetails"),
    path('editdetails/<int:id>/', views.EditDetails.as_view(), name="editdetails"),
    path('account/'  , views.MyAccount.as_view(),name="account"), 
    path('account/myprojects/<int:id>/'  , views.MyAllProjects.as_view(),name="myprojects"), 
    path('account/addproject/' , views.MyProject.as_view(),name="addproject"), 
    path('projects/' , views.AllProjects.as_view(),name="projects"),
    path('devsearch/', views.DevSearch.as_view(),name="devsearch"),
    path('projects/search',views.Search.as_view(), name="search"),
     
]



#  path( 'forget_pass/', views.forget_pass,name="forget_pass"),
#     path('change_pass/<auth_token>/',views.change_pass, name="change_pass"),