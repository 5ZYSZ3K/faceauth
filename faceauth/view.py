import json

from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View


class FaceAuthView(View):
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        try:
            user = User.objects.create_user(username=data['login'], password=data["password"])
        except IntegrityError:
            return HttpResponse('Unauthorized', status=401)
        login(request, user)

        return JsonResponse(
            {"message": "Hello {}".format(user.username)}
        )

    def get(self, request):
        return render(request, "login.html")
