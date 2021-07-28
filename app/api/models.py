from django.db import models


class Visitor(models.Model):
    chat_id = models.IntegerField()

    def __str__(self):
        return str(self.chat_id)

class Booking(models.Model):
    count_people = models.IntegerField()
    booking_time = models.DateTimeField()
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)
