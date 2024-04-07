bookings = [];
function getCookie(name) {
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
    // seats = document.querySelectorAll('.seat');
    // seats.forEach(seat => {
    //     seat.addEventListener('click',()=> onSeatClick(seat));
    // });
    // document.getElementById('book').addEventListener('click',()=> onBook());

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

    document.getElementById('add-schedule')?.addEventListener('click',()=> {
        const cinema = document.getElementById('add-schedule-cinema').value;
        const hall = document.getElementById('add-schedule-hall').value;
        const film = document.getElementById('add-schedule-film').value;
        const time = document.getElementById('add-schedule-time').value;
        fetch('/manage/add-schedule/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                cinema,
                hall,
                film,
                time
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
}

onSeatClick = function(seat) {
    if(seat.dataset.status === 'True') return
    console.log(seat,seat.dataset.number,seat.dataset.status);
    if(seat.classList.contains('selected')) {
        seat.classList.remove('selected');
        index = bookings.indexOf(seat.dataset.number);
        if(index > -1) {
            bookings.splice(index,1);
        }
    } else {
        seat.classList.add('selected');
        bookings.push(seat.dataset.number);
    }
    document.getElementById('book').disabled = bookings.length <= 0;
}
onBook = function() {
    const id = new URLSearchParams(window.location.search).get('id');
    fetch('/book/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,

        },
        body: JSON.stringify({
            'bookings': bookings,
            'id': id,
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
