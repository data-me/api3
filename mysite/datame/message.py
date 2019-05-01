import pytz, datetime
from .models import *
from django.http import JsonResponse
from django.http import JsonResponse
from rest_framework.views import APIView
# Email
from django.core.mail import send_mail
from django.conf import settings
#======

class Notification_view(APIView):
    def post(self, request, format=None):
        try:
            data = request.POST

            subject = data['subject']
            message = data['body']
            email_from = settings.EMAIL_HOST_USER # Email sender
            # Collecting all emails
            all_users = User.objects.all().exclude(id=request.user.id)

            recipient_list = []
            for user in all_users:
                recipient_list.append(user.email)
            #====================
            print(recipient_list)
            # Sending individual email for each user
            for recipient in recipient_list:
                receiver = []
                receiver.append(recipient)
                print('================================')
                send_mail( subject, message, email_from, receiver)
                print('A message was sent')
                print('================================')
            return JsonResponse({"message":"Successfully created new notifications for users"})
        except Exception as e:
            print(e)
            return JsonResponse({"message":"Oops, something went wrong"})


#para dashboard
class Messages_view(APIView):
    def get(self, request, format=None):
        user_logged = User.objects.all().get(pk = request.user.id)
        if (user_logged.is_superuser or user_logged.is_staff):
            try:    
                messages = Message.objects.all().values()
                return JsonResponse(list(messages), safe=False)
            except:
                print("there are no messages")
        return JsonResponse({"message":"Oops, something went wrong"})

class Message_view(APIView):
    def post(self, request, format=None):
        try:
            data = request.POST
            title = data['title']
            body = data['body']
            moment = datetime.datetime.utcnow()
            #receiverId = User.objects.all().get(user = data['receiverId'])
            username = data['username']
            isAlert = False
            receiver = User.objects.all().get(username = username)
            senderId = request.user
            print('Messager senderId =>', senderId)

            new_message = Message.objects.create(title=title, body=body, moment=moment, receiver=receiver, sender=senderId, isAlert= isAlert)

            return JsonResponse({"message":"Successfully created new message"})
        except Exception as e:
            print(e)
            return JsonResponse({"message":"El usuario no existe / User doesn't exists"})
    def get(self, request, format=None):
        try:
            data = request.GET
            user = request.user
            messages = []
            try:
                messages = Message.objects.all().filter(receiver = user).values()
                print(messages)
            except:
                print("You have 0 messages")

            return JsonResponse(list(messages), safe=False)
        except:
            return JsonResponse({"message":"Oops, something went wrong"})
        