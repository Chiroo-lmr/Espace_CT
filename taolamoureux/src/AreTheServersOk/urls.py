from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.AreTheServersOk_index, name="are-the-servers-ok")
]