from django.db import models


# TODO Нормальные имена дать для отображения в Админке


class Visitor(models.Model):
    chat_id = models.IntegerField()

# TODO Переименовать Order в Booking
class Order(models.Model):
    count_people = models.IntegerField()
    time = models.DateTimeField()
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)


# Create your models here.
