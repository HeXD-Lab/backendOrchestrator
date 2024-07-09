from django.urls import path

from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", csrf_exempt(views.index), name="index"),
    path("one/", csrf_exempt(views.speechToText), name="speechToText"),
    path("two/", csrf_exempt(views.processFile), name="processFile"),
    path("three/", csrf_exempt(views.writeFile), name="writeFile"),
]