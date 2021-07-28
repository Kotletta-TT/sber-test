from django.urls import path
from . import views


urlpatterns = [
    path("booking/<int:pk>/", views.GetBookingList.as_view()),
    path("booking/", views.SetBooking.as_view())
]