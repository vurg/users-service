from django.urls import path

from . import views

app_name = "patient"
urlpatterns = [
    # /
    path("", views.index, name="index"),
    path("patient/", views.get_all_patient, name="get_all_patient"),
    path("patient/post", views.post_patient, name="post_patient"),
    path("patient/<uuid:patient_id>", views.get_patient, name="get_patient"),
    path("mqtt/pub", views.publish_message, name="mqtt_pub"),
]
