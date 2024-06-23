from django.urls import path
from .views import *

urlpatterns = [
    path('', Espace_CT_index, name="index"),
    path('About/', About, name="About"),
    path('Projects/', Projects, name="Projects"),
    path('Projects/remove/<str:item_title>', remove_project, name="remove_project"),
    path('Projects/edit_project/<str:item_title>', edit_project, name="edit_project"),
    path('Projects/Counter/', counter, name="counter"),
    path('Projects/IMC_calculator/', IMC, name="IMC"),
    path('Projects/yt-video-importer/', ytVideoImporter, name="yt-video-importer")
]