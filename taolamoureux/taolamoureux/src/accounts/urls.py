from django.urls import path
from .views import *

urlpatterns= [
    path('', redirect_auth, name="login"),
    path('login/', login_user, name="login"),
    path('user/', user, name="user"),
    path('logout/', logout_user, name="logout"),
    path('change_pwd/', change_pwd, name="change_pwd"),
    path('sign_up/', sign_up, name="sign_up"),
    path('sign_up/signup-request/<str:username>', signup_request, name="signup_request"),
]