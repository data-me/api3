import pytz, datetime
from .models import *
from django.http import JsonResponse
from rest_framework.views import APIView
from django.db.models import Q

class Review_view(APIView):
    def post(self, request, format=None):
        try:
            data = request.POST
            reviewedId = data['reviewedId']
            score = data['score']
            comments = data['comments']
            reviewer = User.objects.all().get(pk = request.user.id)
            reviewed = User.objects.all().get(pk = reviewedId)
            if(Review.objects.all().filter(reviewer = reviewer,reviewed = reviewed).exists()):
               return JsonResponse({"message":"User has already reviewed | El usuario ya ha hecho una critica"})
            Review.objects.create(reviewed = reviewed, reviewer = reviewer, score = score, comments = comments)
            
            return JsonResponse({"message":"Successfully created new review"})
        except Exception as e:
            return JsonResponse({"message":"Sorry! Something went wrong... | Oops! Algo ha salido mal..." + str(e)})
class Review_Users_view(APIView):
    def get(self, request, format=None):
        try:
            reviewer = User.objects.all().get(pk = request.user.id)
            users = Review.objects.all().filter(reviewer = reviewer).values("reviewed_id")
            return JsonResponse(list(users), safe=False)
        except Exception as e:
            return JsonResponse({"message":"Sorry! Something went wrong... | Oops! Algo ha salido mal..." + str(e)})

