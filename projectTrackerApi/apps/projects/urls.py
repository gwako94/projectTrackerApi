from django.urls import path
from .views import (
    ProjectAPIView,
    ProjectUpdateDeleteApiView
)


urlpatterns = [
    path('', ProjectAPIView.as_view(), name="projects"),
    path('<id>/', ProjectUpdateDeleteApiView.as_view(), name="fetch-single-project"),
    path('<id>/edit/', ProjectUpdateDeleteApiView.as_view(), name="edit"),
    path('<id>/delete/', ProjectUpdateDeleteApiView.as_view(), name="delete"),
]