from django.urls import path
from . import views
urlpatterns = [
    path("GradeTable", views.GradeTable.as_view()),
]