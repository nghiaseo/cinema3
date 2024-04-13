from datetime import datetime
from typing import List, Dict, Any
from .models import Cinema, Seat, Film, TimeFrame, CinemaHall, Schedule
import math


def get_list_of_cinemas() -> List[any]:
    cinemas = Cinema.objects.all()
    return [{'id': cinema.id, 'name': cinema.name, 'logo': cinema.logo} for cinema in cinemas]


def get_list_of_films() -> List[any]:
    films = Film.objects.all()
    return [{'id': film.id, 'name': film.name, 'poster': film.poster if film.poster else 'movie_default.png'} for film
            in films]


def get_list_of_time_frames() -> List[any]:
    time_frames = TimeFrame.objects.all()
    results = []
    for time_frame in time_frames:
        start_time = time_frame.start_time.strftime('%H:%M')
        end_time = time_frame.end_time.strftime('%H:%M')
        results.append({'id': time_frame.id, 'start_time': start_time, 'end_time': end_time})
    return results


def get_list_of_cinema_halls() -> List[any]:
    halls = CinemaHall.objects.all()
    results = []
    for hall in halls:
        cinema_name = Cinema.objects.get(id=hall.cinema.id).name
        results.append(
            {'id': hall.id, 'name': hall.name, 'cinema_name': cinema_name, 'number_of_seats': hall.number_of_seats,
             'number_of_seats_per_row': hall.number_of_seats_per_row})
    return results


def get_list_of_schedules() -> List[any]:
    schedules = Schedule.objects.all()
    results = []
    for schedule in schedules:
        film_name = Film.objects.get(id=schedule.film.id).name
        cinema_hall_name = CinemaHall.objects.get(id=schedule.cinema_hall.id).name
        cinema_name = Cinema.objects.get(id=CinemaHall.objects.get(id=schedule.cinema_hall.id).cinema.id).name
        time_frame = TimeFrame.objects.get(id=schedule.time_frame.id)
        start_time = time_frame.start_time.strftime('%H:%M')
        end_time = time_frame.end_time.strftime('%H:%M')
        results.append(
            {'id': schedule.id, 'cinema_name': cinema_name, 'film_name': film_name, 'cinema_hall': cinema_hall_name,
             'start_time': start_time,
             'end_time': end_time, 'show_date': schedule.show_date, 'ticket_price': schedule.ticket_price})
    return results


def add_cinema(name: str) -> Dict[str, Any]:
    if name == '':
        return {'error': 'Cinema name cannot be empty'}
    cinema = Cinema.objects.filter(name=name)
    if cinema.exists():
        return {'error': 'Cinema already exists'}
    else:
        cinema = Cinema(name=name)
        cinema.save()
        return {'id': cinema.id, 'name': cinema.name, 'logo': cinema.logo}


def add_film_service(name: str, poster: str) -> Dict[str, Any]:
    if name == '':
        return {'error': 'Film name cannot be empty'}
    film = Film.objects.filter(name=name)
    if film.exists():
        return {'error': 'Film already exists'}
    else:
        film = Film(name=name, poster=poster)
        film.save()
        return {'id': film.id, 'name': film.name, 'poster': film.poster}


def add_time_frame_service(start_time: datetime, end_time: datetime) -> Dict[str, Any]:
    time_frame = TimeFrame(start_time=start_time, end_time=end_time)
    time_frame.save()
    return {'id': time_frame.id, 'start_time': time_frame.start_time, 'end_time': time_frame.end_time}


def add_cinema_hall_service(cinema_id: int, name: str, number_of_seats: int, number_of_seats_per_row: int) -> Dict[
    str, Any]:
    if cinema_id == '':
        return {'error': 'Cinema id cannot be empty'}
    if name == '':
        return {'error': 'Cinema hall name cannot be empty'}
    if number_of_seats == '':
        return {'error': 'Number of seats cannot be empty'}
    if number_of_seats_per_row == '':
        return {'error': 'Number of seats per row cannot be empty'}

    cinema = Cinema.objects.filter(id=cinema_id)
    if not cinema.exists():
        return {'error': 'Cinema does not exist'}

    hall = CinemaHall(name=name, cinema=cinema.first(),
                      number_of_seats=number_of_seats, number_of_seats_per_row=number_of_seats_per_row)
    hall.save()
    return {'id': hall.id, 'name': hall.name, 'cinema': hall.cinema, 'number_of_seats': hall.number_of_seats,
            'number_of_seats_per_row': hall.number_of_seats_per_row}


def add_schedule_service(film_id: int, cinema_hall_id: int, time_frame_id: int, show_date: datetime, ticket_price:float) -> Dict[str, Any]:
    film = Film.objects.filter(id=film_id)
    if not film.exists():
        return {'error': 'Film does not exist'}

    cinema_hall = CinemaHall.objects.filter(id=cinema_hall_id)
    if not cinema_hall.exists():
        return {'error': 'Cinema hall does not exist'}

    time_frame = TimeFrame.objects.filter(id=time_frame_id)
    if not time_frame.exists():
        return {'error': 'Time frame does not exist'}

    schedule = Schedule(film=film.first(), cinema_hall=cinema_hall.first(), time_frame=time_frame.first(),
                        show_date=show_date, ticket_price=ticket_price)
    schedule.save()
    return {'id': schedule.id, 'film': schedule.film, 'cinema_hall': schedule.cinema_hall,
            'time_frame': schedule.time_frame, 'show_date': schedule.show_date}


def update_schedule_service(schedule_id: int, film_id: int, cinema_hall_id: int, time_frame_id: int,
                            show_date: datetime,
                            ticket_price: float) -> Dict[str, Any]:
    schedule = Schedule.objects.filter(id=schedule_id)
    if not schedule.exists():
        return {'error': 'Schedule does not exist'}
    film = Film.objects.filter(id=film_id)
    if not film.exists():
        return {'error': 'Film does not exist'}

    cinema_hall = CinemaHall.objects.filter(id=cinema_hall_id)
    if not cinema_hall.exists():
        return {'error': 'Cinema hall does not exist'}

    time_frame = TimeFrame.objects.filter(id=time_frame_id)
    if not time_frame.exists():
        return {'error': 'Time frame does not exist'}

    schedule = schedule.first()
    schedule.film = film.first()
    schedule.cinema_hall = cinema_hall.first()
    schedule.time_frame = time_frame.first()
    schedule.show_date = show_date
    schedule.ticket_price = ticket_price
    schedule.save()
    return {'id': schedule.id, 'film': schedule.film, 'cinema_hall': schedule.cinema_hall,
            'time_frame': schedule.time_frame, 'show_date': schedule.show_date, 'ticket_price': schedule.ticket_price}
