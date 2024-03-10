from django.shortcuts import render
from django.http import JsonResponse
from .models import File_Details

from django.conf import settings
import os

# Create your views here.
def homepage(request):
   # Query all records from PDF_Details model
    file_details_list = File_Details.objects.all()

    # Prepare a list of dictionaries with 'id' and 'title'
    my_data_list = [
        {'id': file_detail._id, 'title': file_detail.file_name}
        for file_detail in file_details_list
    ]
    context = {'my_data_list': my_data_list}
    return render(request,'pdfchat/index.html',context)

def newChat(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('file')
        if pdf_file:
            try:
                # Create a new PDF_Details instance and save the file
                pdf_details = File_Details(file_name=pdf_file.name)
                pdf_details.file.save(pdf_file.name, pdf_file)

                    # Respond with JSON data
                new_chat = {'id': pdf_details._id, 'title': pdf_details.file_name}
                return JsonResponse(new_chat)

            except Exception as e:
                return JsonResponse({'error': f'Error saving the file: {str(e)}'}, status=500)
        else:
            return JsonResponse({'error': 'No file provided'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def loadChat(request,id):
    my_data_list = [
        {'role': 'user', 'content': 'Hello'},
        {'role': 'assistant', 'content': 'How can I assist you today'},
        {'role': 'user', 'content': 'what is the timing right now'},
        {'role': 'assistant', 'content': "It's 10:30 PM"},
    ]
    response_data = {'id': id, 'messages': my_data_list}
    return JsonResponse(response_data,safe=False)

def getResponse(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chatId')
        message_text = request.POST.get('messageText')
        print(chat_id,message_text)
        return JsonResponse({'status': 'Data received successfully'})
    return JsonResponse({'error': 'Invalid request method'})