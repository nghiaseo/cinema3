from django.db import models


# Create your models here.
class Cinema(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    logo = models.CharField(max_length=500, null=True)


class CinemaHall(models.Model):
    id: models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    number_of_seats = models.IntegerField()
    number_of_seats_per_row = models.IntegerField()


class Seat(models.Model):
    id = models.AutoField(primary_key=True)
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    number = models.IntegerField()


class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    film = models.ForeignKey('Film', on_delete=models.CASCADE)
    cinema_hall = models.ForeignKey('CinemaHall', on_delete=models.CASCADE)
    time_frame = models.ForeignKey('TimeFrame', on_delete=models.CASCADE)
    show_date = models.DateField()
    ticket_price = models.FloatField(default=0.0)


class BookedSeat(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    booked_by = models.ForeignKey('Spectator', on_delete=models.CASCADE, null=True)


class Film(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    poster = models.CharField(max_length=100)


class TimeFrame(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Spectator(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()


class CinemasIncome(models.Model):
    id = models.AutoField(primary_key=True)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    income = models.FloatField(default=0.0)
    time = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
