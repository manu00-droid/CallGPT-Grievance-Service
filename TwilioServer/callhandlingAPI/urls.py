from django.urls import path
from .import views
urlpatterns = [
    path('answer-call', views.answer_call, name='answer_call_name'),
    path('handle-recording', views.handle_recording, name='handle_recording_name'),
    path('confirm-message', views.confirm_message, name='confirm_message_name'),
]
