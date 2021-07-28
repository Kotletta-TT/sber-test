import json

from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

import api.models
from .models import Booking, Visitor
from .serializers import BookingSerializer

# TODO реализовать валидацию на стороне сервера

class SetBooking(APIView):

    def post(self, request):
        user_data = dict(request.data)
        try:
            visitor = Visitor.objects.get(chat_id=user_data['chat_id'])
        except api.models.Visitor.DoesNotExist:
            visitor = None
        if not visitor:
            visitor = Visitor(chat_id=user_data['chat_id'])
            visitor.save()
        booking_time = datetime.strptime(user_data['booking_time'], "%Y-%m-%d %H:%M:%S")
        new_order = Booking(count_people=user_data['count_people'], booking_time=booking_time, visitor=visitor)
        new_order.save()
        serializer = BookingSerializer(new_order)
        return Response(data="OK")

class GetBookingList(APIView):
    def get(self, request, pk):
        try:
            visitor = Visitor.objects.get(chat_id=pk)
        except api.models.Visitor.DoesNotExist:
            visitor = None
        if not visitor:
            return Response("Для данного пользователя брони нет")
        # TODO можно реализовать еще защитную пагинацию от большого количества
        orders = Booking.objects.filter(visitor__chat_id=pk)
        serializer = BookingSerializer(orders, many=True)
        return Response(serializer.data)