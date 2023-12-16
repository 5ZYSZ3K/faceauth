import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


class FaceAuthView(View):
    def post(self, request):
        data = json.loads(request.body)
        return JsonResponse(
            {"message": "Received POST request with {} login".format(data["login"])}
        )

    def get(self, request):
        return render(request, "login.html")
