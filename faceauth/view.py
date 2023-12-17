import io
import json
import uuid

from django.contrib.auth import login
from django.core.files import File
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from psycopg2 import IntegrityError
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

class CreateUserView(View):
    def post(self, request):
        new_username = request.POST.get('new_username')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.create_user(new_username=new_username, new_password=new_password)
            message = f"User {user.new_username} created successfully!"
            return JsonResponse({"message": message})
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)
