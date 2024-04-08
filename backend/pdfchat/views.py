from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Chat_Details
from . import openai_api_call
import uuid
import os
from django.conf import settings
import tempfile
import base64

def homepage(request):
    file_details_list = Chat_Details.objects.all()
    my_data_list = [{'id': file_detail._id, 'title': file_detail.file_name} for file_detail in file_details_list]
    context = {'my_data_list': my_data_list}
    return render(request,'pdfchat/index.html',context)

def newChat(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            chat_id = uuid.uuid4()
            chat_details = Chat_Details(file_name=file.name)
            chat_details._id = chat_id
            chat_details.save()
            _, extension = os.path.splitext(file.name)
            temp_file = tempfile.NamedTemporaryFile(delete=False, dir=os.path.join(settings.MEDIA_ROOT, 'files'), suffix=extension)
            with open(temp_file.name, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            file_path = os.path.join(settings.MEDIA_ROOT, 'files', temp_file.name)
            assistant_data = openai_api_call.createAssistants(file_path)
            chat_detail = get_object_or_404(Chat_Details, _id=chat_id)
            chat_detail.thread_id = assistant_data['thread_id']
            chat_detail.assistant_id = assistant_data['assistant_id']
            chat_detail.openai_file_id = assistant_data['uploaded_file_id']
            chat_detail.save()
            os.remove(file_path)
            new_chat = {'id': chat_details._id, 'title': chat_details.file_name}
            return JsonResponse(new_chat)
        else:
            return JsonResponse({'error': 'No file provided'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def loadChat(request, id):
    chat_details = get_object_or_404(Chat_Details, _id=id)
    thread_id = chat_details.thread_id
    messages = openai_api_call.getMessages(thread_id)
    response_data = {'id': id, 'messages': messages}
    return JsonResponse(response_data, safe=False)

def getResponse(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chatId')
        message_text = request.POST.get('messageText')
        chat_detail = get_object_or_404(Chat_Details, _id=chat_id)
        reply = openai_api_call.getReply(message_text,chat_detail.thread_id,chat_detail.assistant_id)
        if reply['type'] == "text":
            return JsonResponse({'id':'4','content':{'type':'text','message': reply['message']}})
        else:
            image_base64 = base64.b64encode(reply['image']).decode('utf-8')
            return JsonResponse({'id':'4','content':{'type':'image','image':image_base64}})

def deleteChat(request,id):
    chat_detail = get_object_or_404(Chat_Details, _id=id)
    chat_detail.delete()
    return JsonResponse({'message':'chat deleted'})
    
def updateChat(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chatId')
        new_name = request.POST.get('new_name')
        chat_detail = get_object_or_404(Chat_Details, _id=chat_id)
        chat_detail.file_name = new_name
        chat_detail.save()
        return JsonResponse({'message':'success'})
    else:
        # Handle other HTTP methods if needed
        return JsonResponse({'error': 'Invalid request method'}, status=405)



