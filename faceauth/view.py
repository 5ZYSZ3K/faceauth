import io
import json

from django.contrib.auth import authenticate, login
from django.core.files import File
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
import uuid

from rest_framework.authtoken.admin import User
from rest_framework.permissions import IsAuthenticated

from faceauth.models import FacePhoto


class VideoView(View):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        face_photo_instance = FacePhoto(embedding=[hash(request.body)], user=request.user)
        file_name = f"{str(uuid.uuid4())}.jpg"
        with io.BytesIO(request.body) as stream:
            django_file = File(stream)
            face_photo_instance.image.save(file_name, django_file)
        return JsonResponse(
            {"message": "Successful!"}
        )

    def get(self, request):
        return render(request, "video.html")


class LoginView(View):
    def post(self, request):
        user_data = json.loads(request.body)
        user = authenticate(username=user_data['login'], password=user_data['password'] )
        if user is not None:
            login(request, user)
            return JsonResponse(
                {'message': 'user successfully logged in'}
            )
        else:
            return HttpResponse('Unauthorized - wrong password or no user', status=401)

    def get(self, request):
        return render(request, "login.html")


class CreateUserView(View):
    def post(self, request):
        user_data = json.loads(request.body)
        try:
            user = User.objects.create_user(username=user_data['login'], password=user_data['password'])
            login(request, user)
            return JsonResponse(
                {'message': 'user successfully registered'}
            )
        except:
            return HttpResponse('Unauthorized - login already exists', status=401)

    def get(self, request):
        return render(request, "create_user.html")
