from django.urls import path

from . import views

urlpatterns = [
    path("recording", views.get_recording_url, name="get_reccording_url"),
    path("translate",views.translate,name="translate_text"),
]