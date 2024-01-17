from rest_framework.routers import DefaultRouter

from patient.views import PatientView
from tracker.views import MoodTrackerView
from treatment.views import TreatmentView

patient_router = DefaultRouter()
patient_router.register(r"patient", PatientView, basename="patient")
patient_router.register(r"patient/(?P<patient_pk>[^/.]+)/treatment", TreatmentView, basename="treatment")
patient_router.register(r"patient/(?P<patient_pk>[^/.]+)/tracker", MoodTrackerView, basename="tracker")
