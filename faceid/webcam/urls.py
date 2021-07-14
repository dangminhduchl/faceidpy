from django.urls import path
from. import views
from webcam.views import index, video_feed


urlpatterns = [
    path('',views.index),
    path('video_feed/', video_feed, name="video-feed"),
    #path('faceregister/',views.index2)
]