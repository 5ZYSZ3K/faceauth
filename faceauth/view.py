import io

from django.core.files import File
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import uuid
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
    def get(self, request):
        return render(request, "login.html")


class CreateUserView(View):
    def get(self, request):
        return render(request, "create_user.html")
