from django.urls import path
from . import views


urlpatterns = [
    path("booking/<int:pk>/", views.GetOrderList.as_view()),
    path("booking/", views.SetOrder.as_view())
]