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
    seats = document.querySelectorAll('.seat');
    seats.forEach(seat => {
        seat.addEventListener('click',()=> onSeatClick(seat));
    });
    document.getElementById('book').addEventListener('click',()=> onBook());
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
