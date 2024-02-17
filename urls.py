
# from django.conf.urls import url, include
from django.urls import path

from transcript import views

urlpatterns = [
    path('transcript', views.transcript),
    path('subtitles', views.subtitles),
]
