from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.

from mqtt_handler import MQTTHandler

broker_address = "broker.emqx.io"
port = 1883
topic = "Userservice"
# username = "hivemq.webclient.1699615123087"
# password = "Hqd:<e;24G!I7wABkvL9"
mqtt_handler = MQTTHandler(broker_address, port, topic)
mqtt_handler.connect()


def mqtt_connect(request):
    # Initialize MQTTHandler with your broker address, port, and topic

    # Connect to the MQTT broker
    # Perform other tasks...

    # Disconnect from the MQTT broker when done
    # mqtt_handler.disconnect()

    return HttpResponse("MQTT")


def index(request):
    return HttpResponse("Patient app is running")


def publish_message(request):
    # Initialize MQTTHandler with your broker address, port, and topic

    # mqtt_handler = MQTTHandler(broker_address, port, topic)
    # mqtt_handler.connect()

    # Publish a message to the specified topic
    message = "Hello, MQTT!"
    try:
        message_info = mqtt_handler.client.publish(topic, message)
        message_info.wait_for_publish(1.5)
    except TimeoutError as err:
        return JsonResponse(err)

    # Disconnect from the MQTT broker
    # mqtt_handler.disconnect()

    return HttpResponse(message_info.is_published())
