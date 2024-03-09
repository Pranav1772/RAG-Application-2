from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def homepage(request):
    return render(request,'pdfchat/index.html')

def newChat(request):
    newchat={'id': 1, 'title': 'Something'}
    return JsonResponse(newchat)

def loadChat(request,id):
    my_data_list = [
        {'role': 'user', 'content': 'Hello'},
        {'role': 'assistant', 'content': 'How can I assist you today'},
        {'role': 'user', 'content': 'what is the timing right now'},
        {'role': 'assistant', 'content': "It's 10:30 PM"},
    ]
    print(id)
    return JsonResponse(my_data_list,safe=False)

def conversations(request):
    my_data_list = [
        {'id': 1, 'title': 'Something'},
        {'id': 2, 'title': 'Something'},
        {'id': 3, 'title': 'Something'}
    ]
    return JsonResponse(my_data_list)