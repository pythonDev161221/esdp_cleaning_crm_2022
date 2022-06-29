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

async function modalSubmit(modal, method) {
    let uri = window.location.origin;
    let path = $(modal).find('button[type=submit]').data('action')
    let formData = new FormData();
    let csrftoken = getCookie('csrftoken');
    let url = uri + path
    let headers = new Headers();
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

function modalOpen(modal, path, method) {
    initButtonModalDismiss(modal);
    $(modal).find('button[type=submit]').attr('data-action', `${path}`).click(function (e) {
        e.preventDefault();
        modalSubmit(modal, method);
    });
    $('#mask').css({
        'width': $(window).width(),
        'height': $(window).height()
    }).fadeIn(5).fadeTo(200, 0.5);
    $(modal).fadeIn(200);
}

function initButtonModalDismiss(modal) {
    $(modal).find('[data-modal-dismiss]').click(function (e) {
        e.preventDefault();
        $(modal).find('button[type=submit]').off('click');
        $('#mask').hide();
        $(modal).hide();
    });
}

async function initiModalOpenButtons() {
    $('a[data-modal-toggle=update], a[data-modal-toggle=create], a[data-modal-toggle=delete]').click(function (e) {
        e.preventDefault();
        let modal, path, method;
        modal = $(this).data('modal-target');
        path = $(this).data('action');
        if ($(this).data('modal-toggle') === 'update') {
            setFormData(path, modal)
            method = 'PUT'
        } else if ($(this).data('modal-toggle') === 'create') {
            method = 'POST'
        } else if ($(this).data('modal-toggle') === 'delete') {
            $(modal).find("span[id=object-text-name]").text($("a[data-object-name]").data("objectName"))
            method = 'DELETE'
        }
        modalOpen(modal, path, method);
    });
}

$(document).ready(function () {
    initiModalOpenButtons();
})
