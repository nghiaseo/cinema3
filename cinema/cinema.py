from typing import List, Dict, Any
from .models import Cinema, Seat,Film,SeatsStatusByFilms
import math


def getCinemaInfo(name: str,film_id:int) -> dict[str, Any]:
    cinema = Cinema.objects.filter(name=name)
    context = {}
    list_of_seats = []
    if cinema.exists():
        #comment
        cinema = cinema.first()
        resutls = [{'name': cinema.name, 'number_of_seats': cinema.number_of_seats,
                    'number_of_seats_per_row': cinema.number_of_seats_per_row}]
        number_of_seats = resutls[0]['number_of_seats']
        number_of_seats_per_row = resutls[0]['number_of_seats_per_row']
        number_of_rows = math.ceil(number_of_seats / number_of_seats_per_row)
        for i in range(number_of_rows - 1, -1, -1):
            seat_in_row = []
            for j in range(number_of_seats_per_row - 1, -1, -1):
                if i * number_of_seats_per_row + j + 1 <= number_of_seats:
                    try:
                        seat = SeatsStatusByFilms.objects.get(seat_id=i * number_of_seats_per_row + j + 1,film_id=film_id)
                        seat_in_row.append(seat)

                    except SeatsStatusByFilms.DoesNotExist:
                        s = SeatsStatusByFilms(seat_id=i * number_of_seats_per_row + j + 1, film_id=film_id, status=False)
                        s.save()
                        seat_in_row.append(s)

            list_of_seats.append(seat_in_row)

        context = {
            'cinema':
                {
                    'name': resutls[0]['name'],
                    'number_of_seats': range(number_of_seats),
                    'number_of_seats_per_row': range(number_of_seats_per_row),
                    'number_of_rows': enumerate(range(number_of_rows)),
                    'seats': list_of_seats
                }
        }

    return context


def getSeatInfo(seat_number: int):
    seat = Seat.objects.filter(number=seat_number)
    context = {}
    if (seat.exists()):
        seat = seat.first()
        resutls = [{'seat_number': seat.number, 'status': seat.booked}]
        context = {
            'seat_number': resutls[0]['seat_number'],
            'status': resutls[0]['status'],
        }

    return context


def bookSeat(seat_number: int,film_id:int):
    try:
        seat = SeatsStatusByFilms.objects.get(seat_id=seat_number,film_id=film_id)
        seat.status = True
        seat.save()
        return True
    except SeatsStatusByFilms.DoesNotExist:
        return False


def getFilms():
    films = Film.objects.all()
    context = {
        'films': []
    }
    if films.exists():
        context = {
            'films': list(films)
        }
    return context
