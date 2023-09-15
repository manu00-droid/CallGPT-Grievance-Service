from django.urls import path
from .import views
urlpatterns = [
    path('abc', views.answer_call, name='answer_call'),
    path('handle-recording', views.handle_recording, name='handle_recording'),
]
