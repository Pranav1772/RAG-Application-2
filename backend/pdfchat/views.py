from django.shortcuts import render
from django.http import JsonResponse
from .models import PDF_Details

from django.conf import settings
import os

# Create your views here.
def homepage(request):
    return render(request,'pdfchat/index.html')

def newChat(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('file')
        if pdf_file:
            try:
                # Create a new PDF_Details instance and save the file
                pdf_details = PDF_Details(file_name=pdf_file.name)
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
    print(id)
    return JsonResponse(my_data_list,safe=False)

def conversations(request):
    my_data_list = [
        {'id': 1, 'title': 'Something'},
        {'id': 2, 'title': 'Something'},
        {'id': 3, 'title': 'Something'}
    ]
    return JsonResponse(my_data_list)