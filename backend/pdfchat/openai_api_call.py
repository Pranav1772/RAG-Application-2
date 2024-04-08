from django.conf import settings
from dotenv import load_dotenv
from openai import OpenAI
import os
import base64

load_dotenv(dotenv_path=os.path.join(settings.BASE_DIR, '.env'))
client = OpenAI()

def createAssistants(file_path):
    uploaded_file = client.files.create(file=open(file_path,"rb"), purpose="assistants")
    my_assistant = client.beta.assistants.create(
                instructions="""
                1. Data Reliance:
                    You will function as a data-driven assistant, solely relying on the information provided in the uploaded files.
                    Your responses must strictly adhere to the content within the files and avoid referencing external knowledge sources like the internet.
                2. Question Answering:
                    You should excel at answering questions based on the data available in the uploaded files.
                3. Image Generation Limitations:
                    When a question necessitates a visual representation, leverage your image generation capabilities to create a corresponding image. Provide a screenshot of the generated image to enhance your response
                4. Clarification Requests:     
                    If a question requires information not present in the files, politely inform the user and attempt to rephrase the question based on the available data.
                5. Response Accuracy:
                    Remember, the accuracy of your responses is directly tied to the accuracy of the data within the uploaded files.
                """,
                name="File handler",
                tools=[{"type": "retrieval"},{"type": "code_interpreter"}],
                model="gpt-3.5-turbo-1106",
                file_ids=[uploaded_file.id]
            )
    thread = client.beta.threads.create()
    print(thread.id)
    my_data = {'assistant_id':my_assistant.id,'thread_id':thread.id,'uploaded_file_id':uploaded_file.id}
    print(my_assistant.id, thread.id,uploaded_file.id)
    return my_data

def getMessages(thread_id):
    messages = client.beta.threads.messages.list(thread_id=thread_id, order="asc", limit=50)
    message_list = []
    count = 0
    for message in messages.data:
        print(message)
        print("\n\nbreak")
        if message.content[0].type == 'text':
            message_list.append({
                'role': message.role,
                'content': {'type':'text','message':message.content[0].text.value}
            })
        elif message.content[0].type == 'image_file':
            image_data = client.files.content(message.content[0].image_file.file_id)
            image_data_bytes = image_data.read()
            image_base64 = base64.b64encode(image_data_bytes).decode('utf-8')
            
            message_list.append({
                'role': message.role,
                'content': {'type':'image','image':image_base64}})
            # with open(f"my-image{count}.png", "wb") as file:
            #     file.write(image_data_bytes)
            count += 1
    return message_list

def getReply(prompt,thread_id,assistant_id):
    message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=prompt,
        )
    run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
    while True:
        runs = client.beta.threads.runs.retrieve(
                run_id=run.id,
                thread_id=thread_id
            )
        if runs.status not in ["queued", "in_progress", "cancelling"]:
            break
    message = client.beta.threads.messages.list(thread_id=thread_id, order="desc", limit=1)
    if message.data[0].content[0].type == 'text':
        print("Response:",message.data[0].content[0].text.value)
        return {"type":"text","message":message.data[0].content[0].text.value}
    else:
        print(message)
        print(message.data[0].content[0].image_file.file_id)
        image = client.files.content(message.data[0].content[0].image_file.file_id)
        image_data_bytes = image.read()
        # with open("my-image.png", "wb") as file:
        #     file.write(image_data_bytes)
        return {"type":"image","image":image_data_bytes}