from django.urls import path
from .views import DiagnosisHistoryView, SingleDiagnosisView


app_name = 'diagnoses'
urlpatterns = [
    path("images/", DiagnosisHistoryView.as_view(), name="diagnosis_history"),
    path("diagnoses/<int:pk>/", SingleDiagnosisView.as_view(), name="single_diagnosis"),
]
