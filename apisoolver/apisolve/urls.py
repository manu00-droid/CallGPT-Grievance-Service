from django.urls import path

from . import views

urlpatterns = [
    path("parse", views.parse_unstructured_text, name="parse_name"),
    path("recording", views.get_recording_url, name="get_reccording_url"),

]