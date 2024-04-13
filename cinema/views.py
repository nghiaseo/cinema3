import math
from datetime import datetime

from django.db import models
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from cinema.cinema import get_list_of_cinemas, add_cinema, add_film_service, get_list_of_films, add_time_frame_service, \
    get_list_of_time_frames, add_cinema_hall_service, get_list_of_cinema_halls, add_schedule_service, \
    get_list_of_schedules, update_schedule_service
import json

from cinema.models import CinemaHall, Schedule, BookedSeat, Seat, CinemasIncome, Cinema


# Create your views here.

def index(request):
    cinemas = get_list_of_cinemas()
    films = get_list_of_films()
    time_frames = get_list_of_time_frames()

    time = []
    now = datetime.now().strftime('%Y-%m-%d')
    for time_frame in time_frames:
        time.append(
            {'id': time_frame['id'], 'start_time': time_frame['start_time'], 'end_time': time_frame['end_time']})
    context = {'cinemas': cinemas, 'films': films, 'time_frames': time, 'now': now}
    return render(request, 'cinema/index.html', context)


def book_ticket(request):
    if request.method == 'GET':
        schedule_id = request.GET.get('id')
        schedule = Schedule.objects.get(id=schedule_id)
        hall = CinemaHall.objects.get(id=schedule.cinema_hall.id)
        total_seats = hall.number_of_seats
        seats_per_row = hall.number_of_seats_per_row
        booked_seats = BookedSeat.objects.filter(schedule=schedule_id)
        hall_seats = []
        seats = Seat.objects.filter(hall=hall)
        if not seats:
            for i in range(total_seats):
                row = math.floor(i / seats_per_row)
                seat = Seat(hall=hall, number=i + 1)
                seat.save()
                if i % seats_per_row == 0:
                    hall_seats.append([])

                hall_seats[row].append({'id': seat.id, 'number': seat.number, 'booked': False})
        else:
            for seat in seats:
                is_booked = False
                for booked_seat in booked_seats:
                    if booked_seat.seat.id == seat.id:
                        is_booked = True
                        break
                row = math.floor((seat.number - 1) / seats_per_row)
                if (seat.number - 1) % seats_per_row == 0:
                    hall_seats.append([])
                hall_seats[row].append({'id': seat.id, 'number': seat.number, 'booked': is_booked})

        return render(request, 'cinema/book-ticket.html',
                      {'total_seats': total_seats, 'seats_per_row': seats_per_row,
                       'hall_seats': hall_seats, 'schedule': schedule})
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        schedule_id = body['schedule_id']
        seats_id = body['bookings']
        total_price = body['total']
        schedule = Schedule.objects.get(id=schedule_id)
        for seat_id in seats_id:
            seat = Seat.objects.get(id=seat_id)
            booked_seat = BookedSeat(seat=seat, schedule=schedule)
            booked_seat.save()
        cinema_id = schedule.cinema_hall.cinema.id
        income = CinemasIncome(cinema_id=cinema_id, income=total_price)
        income.save()
        return HttpResponse(status=200)


def manage(request):
    cinemas = get_list_of_cinemas()
    films = get_list_of_films()
    time_frames = get_list_of_time_frames()
    rooms = get_list_of_cinema_halls()
    schedules = get_list_of_schedules()
    # get income grouped by cinema not paid
    income = (CinemasIncome.objects.filter(paid=False).values('cinema_id')
              .annotate(total_income=models.Sum('income')))
    income_list = []
    for i in income:
        cinema = Cinema.objects.get(id=i['cinema_id'])
        income_list.append({'cinema': cinema.name, 'income': i['total_income']})

    context = {'cinemas': cinemas, 'films': films, 'time_frames': time_frames, 'rooms': rooms,
               'schedules': schedules, 'income_list': income_list}
    return render(request, 'cinema/manage.html', context)


def make_list_shedule(schedules):
    schedule = []
    for s in schedules:
        cinema_name = s.cinema_hall.cinema.name
        schedule.append({
            'id': s.id,
            'cinema': cinema_name,
            'hall': s.cinema_hall.name,
            'film': s.film.name,
            'start_time': s.time_frame.start_time.strftime('%H:%M'),
            'end_time': s.time_frame.end_time.strftime('%H:%M'),
            'show_date': s.show_date.strftime('%Y-%m-%d'),
            'ticket_price': s.ticket_price
        })
    return schedule


def find_shows(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        cinema_id = body['cinema']
        film_id = body['film']
        # time_frame_id = body['time_frame']
        show_date = body['date']
        schedule = []
        if cinema_id == '' and film_id == '' and show_date == '':
            # get all schedules with show_date >= today
            schedules = Schedule.objects.filter(show_date__gte=datetime.now()).order_by('show_date')
            schedule = make_list_shedule(schedules)
            return HttpResponse(json.dumps(schedule), content_type='application/json', status=200)
        elif cinema_id == '' and film_id == '':
            schedules = Schedule.objects.filter(show_date=show_date).order_by('show_date')
            schedule = make_list_shedule(schedules)
            return HttpResponse(json.dumps(schedule), content_type='application/json', status=200)
        elif cinema_id == '' and show_date == '':
            schedules = Schedule.objects.filter(film=film_id, show_date__gte=datetime.now()).order_by('show_date')
            schedule = make_list_shedule(schedules)
            return HttpResponse(json.dumps(schedule), content_type='application/json', status=200)
        elif film_id == '' and show_date == '':
            halls = CinemaHall.objects.filter(cinema=cinema_id)
            for hall in halls:
                schedules = Schedule.objects.filter(cinema_hall=hall.id, show_date__gte=datetime.now()).order_by('show_date')
                schedule += make_list_shedule(schedules)
            return HttpResponse(json.dumps(schedule), content_type='application/json', status=200)
        elif cinema_id == '':
            schedules = Schedule.objects.filter(film=film_id, show_date=show_date).order_by('show_date')
            schedule = make_list_shedule(schedules)
            return HttpResponse(json.dumps(schedule), content_type='application/json', status=200)
        elif film_id == '':
            halls = CinemaHall.objects.filter(cinema=cinema_id)
            for hall in halls:
                schedules = Schedule.objects.filter(cinema_hall=hall.id, show_date=show_date).order_by('show_date')
                schedule += make_list_shedule(schedules)
            return HttpResponse(json.dumps(schedule), content_type='application/json', status=200)
        elif show_date == '':
            halls = CinemaHall.objects.filter(cinema=cinema_id)
            for hall in halls:
                schedules = Schedule.objects.filter(cinema_hall=hall.id, film=film_id, show_date__gte=datetime.now()).order_by('show_date')
                schedule += make_list_shedule(schedules)
            return HttpResponse(json.dumps(schedule), content_type='application/json', status=200)
        else:
            halls = CinemaHall.objects.filter(cinema=cinema_id)
            for hall in halls:
                schedules = Schedule.objects.filter(cinema_hall=hall.id, film=film_id,
                                                    show_date=show_date)
                schedule += make_list_shedule(schedules)
            return HttpResponse(json.dumps(schedule), content_type='application/json', status=200)


def create_cinema(request):
    if request.method == 'GET':
        return render(request, 'cinema/create-cinema.html')
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        cinema_name = body['name']
        context = add_cinema(cinema_name)
        if context.get('error'):
            # return response with error message
            return HttpResponseBadRequest(json.dumps(context))
        else:
            return HttpResponse(status=200)


def add_film(request):
    if request.method == 'GET':
        return render(request, 'cinema/add-film.html')
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        film_name = body['name']
        poster = body['poster']
        context = add_film_service(film_name, poster)
        if context.get('error'):
            return HttpResponseBadRequest(json.dumps(context))
        else:
            return HttpResponse(status=200)


def add_time_frame(request):
    if request.method == 'GET':
        return render(request, 'cinema/add-time-frame.html')
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        start_time = body['start']
        end_time = body['end']
        formatted_start_time = datetime.now().replace(hour=int(start_time['hour']), minute=int(start_time['minute']))
        formatted_end_time = datetime.now().replace(hour=int(end_time['hour']), minute=int(end_time['minute']))
        add_time_frame_service(formatted_start_time, formatted_end_time)
        return HttpResponse(status=200)


def add_cinema_hall(request):
    if request.method == 'GET':
        context = {'cinemas': get_list_of_cinemas()}
        return render(request, 'cinema/add-cinema-hall.html', context)
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        cinema = body['cinema']
        name = body['name']
        number_of_seats = body['capacity']
        number_of_seats_per_row = body['columns']
        cinema_hall = add_cinema_hall_service(cinema, name, number_of_seats, number_of_seats_per_row)
        if cinema_hall.get('error'):
            return HttpResponseBadRequest(json.dumps(cinema_hall))
        else:
            return HttpResponse(status=200)


def get_halls_by_cinema(request):
    if request.method == 'GET':
        cinema_id = request.GET.get('cinema_id')
        halls = CinemaHall.objects.filter(cinema=cinema_id)
        results = []
        for hall in halls:
            results.append({'id': hall.id, 'name': hall.name})
        return HttpResponse(json.dumps(results), content_type='application/json', status=200)


def add_schedule(request):
    if request.method == 'GET':
        context = {'films': get_list_of_films(),
                   'cinemas': get_list_of_cinemas(),
                   'rooms': get_list_of_cinema_halls(),
                   'time_frames': get_list_of_time_frames()}
        return render(request, 'cinema/add-schedule.html', context)
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        film = body['film']
        cinema_hall = body['hall']
        time_frame = body['time']
        show_date = body['date']
        ticket_price = body['price']
        if film == '' or cinema_hall == '' or time_frame == '' or show_date == '':
            return HttpResponseBadRequest(json.dumps({'error': 'All fields are required'}))
        else:
            add_schedule_service(film, cinema_hall, time_frame, show_date, ticket_price)
            return HttpResponse(status=200)


def edit_schedule(request):
    if request.method == 'GET':
        schedule_id = request.GET.get('id')
        schedule = Schedule.objects.get(id=schedule_id)
        halls = CinemaHall.objects.filter(cinema=schedule.cinema_hall.cinema.id)
        context = {'films': get_list_of_films(),
                   'cinemas': get_list_of_cinemas(),
                   'rooms': get_list_of_cinema_halls(),
                   'time_frames': get_list_of_time_frames(),
                   'schedule': schedule,
                   'date': schedule.show_date.strftime('%Y-%m-%d'),
                   'halls': halls}
        return render(request, 'cinema/add-schedule.html', context)
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        film = body['film']
        cinema_hall = body['hall']
        time_frame = body['time']
        show_date = body['date']
        ticket_price = body['price']
        schedule_id = body['schedule_id']
        if film == '' or cinema_hall == '' or time_frame == '' or show_date == '':
            return HttpResponseBadRequest(json.dumps({'error': 'All fields are required'}))
        else:
            update_schedule_service(schedule_id, film, cinema_hall, time_frame, show_date, ticket_price)
            return HttpResponse(status=200)
