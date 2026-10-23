from django.urls import path

from estimator import views

urlpatterns = [
    path("", views.index, name="index"),
]
