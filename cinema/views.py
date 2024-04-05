from django.shortcuts import render
from cinema.cinema import getCinemaInfo, bookSeat, getFilms
import json


# Create your views here.

def index(request):
    id = request.GET.get('id', None)
    print(id)
    cinema = getCinemaInfo('cgv',id)
    return render(request, 'cinema/index.html', cinema)

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