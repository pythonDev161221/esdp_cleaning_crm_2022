function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function copy_token() {
    const copyBtn = document.getElementById('copy-btn');
    window.addEventListener('click', () => {
        const token = copyBtn.getAttribute('data-token');
        navigator.clipboard.writeText(token);
        copyBtn.textContent = 'Token скопирован';
    })
}

async function modalSubmit(path, method, modal) {
    let uri = window.location.origin;
    let formData = new FormData();
    let csrftoken = getCookie('csrftoken');
    let headers = new Headers();
    let url = uri + path
    headers.append("X-CSRFToken", csrftoken);
    $(modal).find('input, textarea, select').each(function () {
        formData.append(this.name, $(this).val())
    });
    let response = await fetch(url, {
        method: method,
        body: formData,
        headers: headers,
        redirect: 'follow'
    });
    if (response.ok) {
        window.location.reload()
    }
}

function makeSettings(path, method, data) {
    let csrftoken = getCookie('csrftoken')
    let uri = $(location).attr('origin');
    return {
        'url': uri + path,
        'method': method,
        'timeout': 0,
        'headers': {
            'X-CSRFToken': csrftoken
        },
        'processData': false,
        'Content-Type': 'application/json',
        'data': data
    }
}

function setFormData(path, modal) {
    $.ajax(makeSettings(path, 'GET')).done(function (response) {
        $(modal).find('input, textarea, select').each(function () {
            if (this.tagName === 'SELECT') {
                $(this).prepend(`<option value=${response[this.name].id} selected>${response[this.name].name}</option>`)
            } else {
                $(this).attr('value', response[this.name])
            }
        });
    }).fail(function (response, status) {
        console.log(response);
        console.log(status.text);
    });
}

function modalOpen(modal) {
    $('#mask').css({
        'width': $(window).width(),
        'height': $(window).height()
    }).fadeIn(5).fadeTo(200, 0.5);
    $(modal).fadeIn(200);
}

async function initiModalOpenButtons() {
    $('a[data-modal-toggle=update]').click(function (e) {
        e.preventDefault();
        let modal = $(this).data('modal-target');
        let path = $(this).data('action');
        modalOpen(modal)
        setFormData(path, modal)
        $(modal).find('button[type=submit]').click(function (e) {
            e.preventDefault();
            modalSubmit(path, 'PUT', modal)
        });
    });
    $('a[data-modal-toggle=delete]').click(function (e) {
        e.preventDefault();
        let modal = $(this).data('modal-target');
        let path = $(this).data('action');
        modalOpen(modal)
        $(modal).find('button[type=submit]').click(function (e) {
            e.preventDefault();
            modalSubmit(path, 'DELETE', modal);
        });
    });
    $('a[data-modal-toggle=create]').click(function (e) {
        e.preventDefault();
        let modal = $(this).data('modal-target');
        let action = $(this).data('action');
        modalOpen(modal)
        $(modal).find('button[type=submit]').click(function (e) {
            e.preventDefault();
            modalSubmit(action, 'POST', modal);
        });
    });
}

function initButtonModalDissmit () {
    $('[data-modal-dismiss]').click(function (e) {
        e.preventDefault();
        let dismiss = $(this).data('modal-dismiss');
        $('#mask').hide();
        $(dismiss).hide();
    });
}

$(document).ready(function () {
    initiModalOpenButtons();
    initButtonModalDissmit();
})
