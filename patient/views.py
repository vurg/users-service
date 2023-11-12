import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your views here.

from mqtt_handler import MQTTHandler
from .models import Patient


broker_address = "broker.emqx.io"
port = 1883
topic = "Userservice"
# username = "hivemq.webclient.1699615123087"
# password = "Hqd:<e;24G!I7wABkvL9"
mqtt_handler = MQTTHandler(broker_address, port, topic)
mqtt_handler.connect()


def get_all_patient(request):
    patients = Patient.objects.all().values()
    patients_list = list(patients)
    if len(patients_list) == 0:
        return JsonResponse({"message": "No patients found!"}, status=404)
    return JsonResponse({"patients": patients_list}, safe=False, status=200)


def get_patient(request, patient_id):
    try:
        patient = Patient.objects.get(pk=patient_id)
        # TODO: Serialize patient object
        return JsonResponse(patient, safe=False, status=200)
    except Patient.DoesNotExist:
        return JsonResponse({"message": "Patient not found!"}, status=404)
    except Exception as e:
        print("Error: ", e)
        return JsonResponse({"message": str(e)}, status=500)


@csrf_exempt
def post_patient(request):
    try:
        data = json.loads(request.body)
        if not data["name"]:
            raise ValidationError("Name is required")
        if not data["email"]:
            raise ValidationError("Email is required")
        if not data["password"]:
            raise ValidationError("Password is required")
        validate_email(data["email"])  # From django.core.validators

        new_patient = Patient(
            name=data["name"],
            email=data["email"],
            password=data["password"],
        )
        new_patient.save()
        return JsonResponse({"message": "Patient was added successfully!"}, status=201)
    except ValidationError as e:
        return JsonResponse({"message": e.message}, status=400)
    except KeyError as e:
        return JsonResponse({"message": f"{str(e)} is required"}, status=400)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)


def index(request):
    return HttpResponse("Patient app is running")


def publish_message(request):
    # Publish a message to the specified topic
    message = "Hello, MQTT!"
    try:
        message_info = mqtt_handler.client.publish(topic, message)
        message_info.wait_for_publish(1.5)
    except TimeoutError as err:
        return JsonResponse(err)
    return HttpResponse(message_info.is_published())
