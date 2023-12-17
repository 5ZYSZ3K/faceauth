from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


class VideoView(View):
    def post(self, request):
        print(request.body)
        print(hash(request.body))
        return JsonResponse(
            {"message": "Hello XD"}
        )

    def get(self, request):
        return render(request, "video.html")
