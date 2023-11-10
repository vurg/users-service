from django.urls import path

from . import views

app_name = "patient"
urlpatterns = [
    # /
    path("", views.index, name="index"),
    path("mqtt", views.mqtt_connect, name="mqtt"),
    path("mqtt/pub", views.publish_message, name="mqtt_pub"),
]
