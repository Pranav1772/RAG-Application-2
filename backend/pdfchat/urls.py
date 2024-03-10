from django.urls import path
from pdfchat import views

urlpatterns = [
    path("", views.homepage,name='homepage'),
    path("new_chat/",views.newChat,name='newChat'),
    path("load_chat/<int:id>/",views.loadChat,name='newChat'),
    path("get_response/",views.getResponse,name='getResponse'),
]
