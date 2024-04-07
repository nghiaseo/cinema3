from datetime import datetime
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from cinema.cinema import get_list_of_cinemas, add_cinema, add_film_service, get_list_of_films, add_time_frame_service, \
    get_list_of_time_frames, add_cinema_hall_service, get_list_of_cinema_halls
import json

from cinema.models import CinemaHall


# Create your views here.

def index(request):
    cinemas = get_list_of_cinemas()
    context = {'cinemas': cinemas}
    return render(request, 'cinema/index.html', context)


def manage(request):
    cinemas = get_list_of_cinemas()
    films = get_list_of_films()
    time_frames = get_list_of_time_frames()
    rooms = get_list_of_cinema_halls()

    context = {'cinemas': cinemas, 'films': films, 'time_frames': time_frames, 'rooms': rooms}
    return render(request, 'cinema/manage.html', context)


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
        cinema_hall = body['room']
        time_frame = body['time_frame']
        show_date = body['show_date']
        return HttpResponse(status=200)


'''
def book(request):
    if request.method == 'POST':
        seats_number = request.body
        body = json.loads(seats_number.decode('utf-8'))
        list_bookings = body['bookings']
        film_id = int(body['id'])
        for booking in list_bookings:
            bookSeat(booking,film_id)
        cinema = getCinemaInfo('cgv',film_id)
        return render(request, 'cinema/index.html', cinema)

def showing(request):
    context = getFilms()
    return render(request, 'cinema/showing.html',context)
'''
