let bookings = [];
let total = 0;
function getCookie(name) {
    console.log('getCookie',document.cookie);
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
window.onload = function() {
    bookings = [];
    const seats = document.querySelectorAll('.seat');
    seats.forEach(seat => {
        seat.addEventListener('click',()=> onSeatClick(seat));
    });
    document.getElementById('btn-confirm-book')?.addEventListener('click',()=> onBook());

    // add event listener to the save-cinema button
    document.getElementById('save-cinema')?.addEventListener('click',()=> {
        const name = document.getElementById('create-cinema-name').value;

        fetch('/manage/create-cinema/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'name': name
            })
        })
        .then(data => {
            if(data.status === 200) {
                location.href = '/manage';
            } else {
                // read body of the response
                data.json().then(data => {
                    const error = document.getElementById('create-cinema-error');
                    error.innerText = data.error;
                });
            }
        })
    });

    //handle the create-cinema form
    document.getElementById('create-cinema-name')?.addEventListener('input',()=> {
        const error = document.getElementById('create-cinema-error');
        error.innerText = '';
    })

    // add event listener to the add-film button
    document.getElementById('add-film')?.addEventListener('click',()=> {
        const name = document.getElementById('add-film-name').value;
        const poster = document.getElementById('add-film-poster').value;
        fetch('/manage/add-film/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                 name,
                poster
            })
        })
        .then(data => {
            if(data.status === 200) {
                location.href = '/manage';
            } else {
                // read body of the response
                data.json().then(data => {
                    const error = document.getElementById('add-film-error');
                    error.innerText = data.error;
                });
            }
        })
    });

    //add event listener to the add-time-frame button
    document.getElementById('add-time-frame')?.addEventListener('click',()=> {
        const start_time = document.getElementById('add-time-frame-start').value+'';
        const end_time = document.getElementById('add-time-frame-end').value;
        const start = {
            hour: parseInt(start_time.split(':')[0]),
            minute: parseInt(start_time.split(':')[1])
        }
        const end = {
            hour: parseInt(end_time.split(':')[0]),
            minute: parseInt(end_time.split(':')[1])
        }
        if(start.hour > end.hour || (start.hour === end.hour && start.minute >= end.minute)) {
            const error = document.getElementById('add-time-frame-error');
            error.innerText = 'Invalid time frame';
            return
        }

        fetch('/manage/add-time-frame/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                start,
                end
            })
        })
        .then(data => {
            if(data.status === 200) {
                location.href = '/manage';
            } else {
                // read body of the response
                data.json().then(data => {
                    const error = document.getElementById('add-time-frame-error');
                    error.innerText = data.error;
                });
            }
        })
    });

    //add event listener to the add-cinema-hall button
    document.getElementById('add-cinema-hall')?.addEventListener('click',()=> {
        const cinema = document.getElementById('select-cinema').value;
        const name = document.getElementById('add-hall-name').value;
        const capacity = document.getElementById('add-hall-size').value;
        const columns = document.getElementById('add-hall-row-size').value;

        fetch('/manage/add-cinema-hall/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                cinema,
                name,
                capacity,
                columns
            })
        })
        .then(data => {
            if(data.status === 200) {
                location.href = '/manage';
            } else {
                // read body of the response
                data.json().then(data => {
                    const error = document.getElementById('add-cinema-hall-error');
                    error.innerText = data.error;
                });
            }
        })
    })

    //add event listener to the add-schedule
    document.getElementById(('add-schedule-cinema'))?.addEventListener('change',()=> {
        const cinema = document.getElementById('add-schedule-cinema').value;
        const select = document.getElementById('add-schedule-hall');
        if(cinema === '') {
            select.innerHTML = '';
            return
        }
        fetch(`/manage/get-halls-by-cinema/?cinema_id=${cinema}`)
        .then(data => data.json())
        .then(data => {
            select.innerHTML = '';
            data.forEach(hall => {
                const option = document.createElement('option');
                option.value = hall.id;
                option.innerText = hall.name;
                select.appendChild(option);
            })
        })
    })

    document.getElementById('add-schedule')?.addEventListener('click',(event)=> {
        const hall = document.getElementById('add-schedule-hall').value;
        const film = document.getElementById('add-schedule-film').value;
        const time = document.getElementById('add-schedule-time').value;
        const date = document.getElementById('add-schedule-date').value;
        const price = document.getElementById('add-schedule-price').value;
        const schedule_id = event.target.dataset.scheduleId;
        if(schedule_id) {
            fetch('/manage/edit-schedule/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    date,
                    hall,
                    film,
                    time,
                    schedule_id,
                    price
                })
            })
            .then(data => {
                if(data.status === 200) {
                    location.href = '/manage';
                } else {
                    // read body of the response
                    data.json().then(data => {
                        const error = document.getElementById('add-schedule-error');
                        error.innerText = data.error;
                    });
                }
            })
        }
        else
        fetch('/manage/add-schedule/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                date,
                hall,
                film,
                time,
                price
            })
        })
        .then(data => {
            if(data.status === 200) {
                location.href = '/manage';
            } else {
                // read body of the response
                data.json().then(data => {
                    const error = document.getElementById('add-schedule-error');
                    error.innerText = data.error;
                });
            }
        })
    })

    //add event listener to the find-shows button
    document.getElementById('find-shows')?.addEventListener('click',()=> {
        const cinema = document.getElementById('cinema').value;
        const film = document.getElementById('film').value;
        // const time_frame = document.getElementById('time_frame').value;
        const date = document.getElementById('date').value;
        fetch('/find-shows/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                cinema,
                film,
                // time_frame,
                date
            })
        }) .then(data => {
        if(data.status === 200) {
            data.json().then(data => {
                presentShow(data);
            });
        } else {
            // read body of the response
            data.json().then(data => {
                const error = document.getElementById('index-error');
                error.innerText = data.error;
            });
        }
    })
    })

    //add event listener to the cancel button
    document.getElementById('cancel')?.addEventListener('click',()=> {
        document.getElementById('cancel').classList.remove('show');
        bookings = [];
        document.querySelectorAll('.selected').forEach(seat => {
            seat.classList.remove('selected');
        })
        const confirmBtn = document.getElementById('confirmBtn');
        confirmBtn.disabled = true;

    })

    //add event listener to the edit schedule buttons
    document.querySelectorAll('.btn-edit-schedule')?.forEach(button => {
        button.addEventListener('click',()=> {
            const id = button.dataset.scheduleId;
            window.location.href = `/manage/edit-schedule/?id=${id}`;
        })
    })

    //get all available shows
    getAllAvailableShows()

    //add event listener to the confirmModal
    const modal =document.getElementById('confirmModal')
    modal?.addEventListener('show.bs.modal', function (event) {
        const message = document.getElementById('booking-message');
        message.innerText = 'You are about to book '+bookings.length+' seats : '+bookings.join(',');
        total = bookings.length * price;
        const totalPrice = document.getElementById('total-price');
        totalPrice.innerText = 'Total Price: '+total;
    })
}

getAllAvailableShows = function() {
    fetch('/find-shows/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            cinema:'',
            date:'',
            film:''
        })
    }) .then(data => {
        if(data.status === 200) {
            data.json().then(data => {
                presentShow(data);
            });
        } else {
            // read body of the response
            data.json().then(data => {
                const error = document.getElementById('index-error');
                error.innerText = data.error;
            });
        }
    })

}

presentShow = function(data) {
    const table = document.getElementById('find-shows-table');
    if(!table) return
                table.innerHTML = '';
                const header = document.createElement('tr');
                const cinema_header = document.createElement('th');
                cinema_header.innerText = 'Cinema';
                header.appendChild(cinema_header);
                const hall_header = document.createElement('th');
                hall_header.innerText = 'Hall';
                header.appendChild(hall_header);
                const film_header = document.createElement('th');
                film_header.innerText = 'Film';
                header.appendChild(film_header);
                const date_header = document.createElement('th');
                date_header.innerText = 'Date';
                header.appendChild(date_header);
                const start_header = document.createElement('th');
                start_header.innerText = 'Start Time';
                header.appendChild(start_header);
                const end_header = document.createElement('th');
                end_header.innerText = 'End Time';
                header.appendChild(end_header);
                const price_header = document.createElement('th');
                price_header.innerText = 'Price';
                header.appendChild(price_header);
                const book_header = document.createElement('th');
                book_header.innerText = 'Book';
                header.appendChild(book_header);
                table.appendChild(header);
                data.forEach(show => {
                    const row = document.createElement('tr');
                    const cinema = document.createElement('td');
                    cinema.innerText = show.cinema;
                    row.appendChild(cinema);
                    const hall_name = document.createElement('td');
                    hall_name.innerText = show.hall;
                    row.appendChild(hall_name);
                    const film = document.createElement('td');
                    film.innerText = show.film;
                    row.appendChild(film);
                    const date = document.createElement('td');
                    date.innerText = show.show_date;
                    row.appendChild(date);
                    const start = document.createElement('td');
                    start.innerText = show.start_time;
                    row.appendChild(start);
                    const end = document.createElement('td');
                    end.innerText = show.end_time;
                    row.appendChild(end);
                    const price = document.createElement('td');
                    price.innerText = show.ticket_price
                    row.appendChild(price);
                    const book = document.createElement('td');
                    const button = document.createElement('button');
                    button.className = 'btn btn-primary';

                    button.innerText = 'Book';
                    button.addEventListener('click',()=> {
                        location.href = `/book-ticket/?id=${show.id}`;
                    })
                    book.appendChild(button);
                    row.appendChild(book);
                    table.appendChild(row);
                })
}

onSeatClick = function(seat) {
    if(seat.dataset.status === 'True') return
    if(seat.classList.contains('selected')) {
        seat.classList.remove('selected');
        const index = bookings.indexOf(seat.dataset.number);
        if(index > -1) {
            bookings.splice(index,1);
        }
    } else {
        seat.classList.add('selected');
        bookings.push(seat.dataset.number);
    }
    if(document.getElementById('confirmBtn'))
    document.getElementById('confirmBtn').disabled = bookings.length <= 0;
    const btnCancel = document.getElementById('cancel');
    if(btnCancel) {
        if(bookings.length > 0)
        btnCancel.classList.add('show');
        else
        btnCancel.classList.remove('show');
    }

}
onBook = function() {
    const id = new URLSearchParams(window.location.search).get('id');
    fetch('/book-ticket/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,

        },
        body: JSON.stringify({
            'bookings': bookings,
            'schedule_id': id,
            'total': total
        })
    })
    .then(data => {
        if(data.status === 200) {
        console.log('Booking Success');
            location.reload();
        } else {
            console.log('Booking Failed');
        }
    })
}
