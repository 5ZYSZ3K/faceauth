import io
import json

from PIL import Image
from django.contrib.auth import authenticate, login
from django.core.files import File
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
import uuid

from django.views.decorators.csrf import csrf_exempt
from facenet_pytorch.models.inception_resnet_v1 import InceptionResnetV1
from facenet_pytorch.models.mtcnn import MTCNN
from pgvector.django import L2Distance
from rest_framework.authtoken.admin import User
from rest_framework.permissions import IsAuthenticated

from faceauth.models import FacePhoto


mtcnn = MTCNN(image_size=160, margin=20)
resnet = InceptionResnetV1(pretrained='vggface2').eval()


class LoginVideoView(View):
    @csrf_exempt
    def post(self, request):
        user_login = request.POST.get("login")
        user = User.objects.filter(username=user_login).first()
        image = Image.open(request.FILES['image']).convert('RGB')
        if image is None or user is None:
            return HttpResponseBadRequest("Incorrect data!")
        file_name_core = str(uuid.uuid4())
        django_file = File(request.FILES['image'])
        img_cropped = mtcnn(image, save_path=f"./static/{file_name_core}-processed.jpg")
        if img_cropped is None:
            return HttpResponseBadRequest("No face detected!")
        img_embedding = resnet(img_cropped.unsqueeze(0))
        nearest_neighbours = FacePhoto.objects.filter(user=user)\
            .alias(distance=L2Distance('embedding', img_embedding[0])).filter(distance__lt=0.5)
        if len(nearest_neighbours) > 0:
            face_photo_instance = FacePhoto(embedding=img_embedding[0], user=user)
            face_photo_instance.image.save(f"{file_name_core}.jpg", django_file)
            login(request, user)
            return JsonResponse(
                {"message": "Successful!"}
            )
        else:
            return HttpResponseBadRequest("Could not match the face!")

    def get(self, request):
        return render(request, "video.html")


class LoginView(View):
    @csrf_exempt
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
    @csrf_exempt
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


class AddVideoView(View):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request):
        with io.BytesIO(request.body) as stream:
            if stream is None:
                return HttpResponseBadRequest("Incorrect data!")
            file_name_core = str(uuid.uuid4())
            django_file = File(stream)
            image = Image.open(stream).convert('RGB')
            img_cropped = mtcnn(image, save_path=f"./static/{file_name_core}-processed.jpg")
            if img_cropped is None:
                return HttpResponseBadRequest("No face detected!")
            img_embedding = resnet(img_cropped.unsqueeze(0))
            face_photo_instance = FacePhoto(embedding=img_embedding[0], user=request.user)
            face_photo_instance.image.save(f"{file_name_core}.jpg", django_file)
            return JsonResponse(
                {"message": "Successful!"}
            )

    def get(self, request):
        return render(request, "add_video.html")

