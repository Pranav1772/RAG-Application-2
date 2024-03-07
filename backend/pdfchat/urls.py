from django.urls import path
from pdfchat import views

urlpatterns = [
    path("", views.Homepage,name='homepage'),
]
