from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Chat_Details
import uuid
from django.shortcuts import get_object_or_404
import json
from io import BytesIO
from PIL import Image

from django.conf import settings
import os
from dotenv import load_dotenv
from openai import OpenAI
import tempfile


load_dotenv(dotenv_path=os.path.join(settings.BASE_DIR, '.env'))
client = OpenAI()




# Create your views here.
def homepage(request):
   # Query all records from PDF_Details model
    file_details_list = Chat_Details.objects.all()

    # Prepare a list of dictionaries with 'id' and 'title'
    my_data_list = [
        {'id': file_detail._id, 'title': file_detail.file_name}
        for file_detail in file_details_list
    ]
    context = {'my_data_list': my_data_list}
    return render(request,'pdfchat/index.html',context)

def newChat(request):   
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            # try:
            chat_id = uuid.uuid4()
            chat_details = Chat_Details(file_name=file.name)
            chat_details._id = chat_id
            chat_details.save()
            _, extension = os.path.splitext(file.name)
            temp_file = tempfile.NamedTemporaryFile(delete=False,dir=os.path.join(settings.MEDIA_ROOT, 'files'),suffix=extension)
            print(temp_file.name)
            
            with open(temp_file.name, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            file_path = os.path.join(settings.MEDIA_ROOT, 'files', temp_file.name)
            
            uploaded_file=client.files.create(
                    file=open(file_path,"rb"),
                    purpose="assistants",)
            os.remove(file_path)
            
            my_assistant = client.beta.assistants.create(
            instructions="You have access to the files to answer user questions about company information. Extract the text from each file and use the content from the file to answer each question and when data visualization is asked then create it and always upload the file and it should alway be in Image(PNG) format provide it with file path",
            name="File handler",
            tools=[{"type": "retrieval"},{"type": "code_interpreter"}],
            model="gpt-3.5-turbo-1106",
            file_ids=[uploaded_file.id]
            )
            thread = client.beta.threads.create()
            
            
            
            chat_detail = get_object_or_404(Chat_Details,_id=chat_id)
            chat_detail.thread_id = thread.id
            chat_detail.assistant_id = my_assistant.id
            chat_detail.openai_file_id=uploaded_file.id
            chat_detail.save()
            new_chat = {'id': chat_details._id, 'title': chat_details.file_name}
            return JsonResponse(new_chat)

            # except Exception as e:
            #     return JsonResponse({'error': f'Error saving the file: {str(e)}'}, status=500)
        else:
            return JsonResponse({'error': 'No file provided'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def loadChat(request,id):
    print('its here')
    chat_details = get_object_or_404(Chat_Details,_id=id)
    thread_id = chat_details.thread_id
    messages = client.beta.threads.messages.list(thread_id=thread_id,order="asc",limit=50)

    message_list=[]
    count = 0
    for message in messages.data:
        # print(message)
        # Check if the content is text or image_file
        if message.content[0].type == 'text':
            message_list.append({
                'role':message.role,
                'content':message.content[0].text.value
            })
        elif message.content[0].type == 'image_file':
            message_list.append({
                'role':message.role,
                'content':message.content[0].image_file.file_id
            })
            image_data = client.files.content(message.content[1].text.annotations[0].file_path.file_id)
            image_data_bytes = image_data.read()
            with open("my-image"+str(count)+".png", "wb") as file:
                file.write(image_data_bytes)
            count=+1
    print(id)
    
    # image_data_bytes = image_data.read()
    # print(type(image_data_bytes))
    # with open("my-image.png", "wb") as file:
    #     file.write(image_data_bytes)
    response_data = {'id': id, 'messages': message_list}
    return JsonResponse(response_data,safe=False)

def getResponse(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chatId')
        message_text = request.POST.get('messageText')
        print(chat_id,message_text)
        chat_detail = get_object_or_404(Chat_Details,_id=chat_id)
        
        message = client.beta.threads.messages.create(
            thread_id = chat_detail.thread_id,
            role="user",
            content=message_text,
        )
        run = client.beta.threads.runs.create(
            thread_id=chat_detail.thread_id,
            assistant_id=chat_detail.assistant_id
        )
        while True:
            runs = client.beta.threads.runs.retrieve(
                run_id=run.id,
                thread_id=chat_detail.thread_id
            )
            if runs.status not in ["queued","in_progress","cancelling"]:
                break
        
        message = client.beta.threads.messages.list(thread_id=chat_detail.thread_id,order="desc",limit=1)
        if message.data[0].content[0].type == 'text':
            print(message.data[0].content[0].text.value)
            # # response= "<pre>"+message.data[0].content[0].text.value+"</pre>"
            # return HttpResponse(message.data[0].content[0].text.value)
            return JsonResponse({'status': message.data[0].content[0].text.value})    
        else:
            print(message)
            print((client.files.retrieve(message.data[0].content[0].image_file.file_id)).bytes)
            print(message.data[0].content[0].image_file.file_id)
            image=client.files.content(message.data[0].content[1].text.annotations[0].file_path.file_id)
            image_data_bytes = image.read()
            print(type(image_data_bytes))
            with open("my-image.png", "wb") as file:
                file.write(image_data_bytes)
            return JsonResponse({'status': message.data[0].content[0].image_file.file_id})
        
        
    return JsonResponse({'error': 'Invalid request method'})