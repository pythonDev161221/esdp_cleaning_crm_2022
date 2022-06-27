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

function copy_token(event) {
    const copyBtn = document.getElementById('copy-btn');
    window.addEventListener('click', () => {
        const token = copyBtn.getAttribute('data-token');
        navigator.clipboard.writeText(token);
        copyBtn.textContent = 'Token скопирован';
    })
}

async function requestOnCreate(path, formSelector) {
    let baseUri = window.location.origin;
    let formData = new FormData();
    $(formSelector).find('input, textarea, select').each(function () {
        formData.append(this.name, $(this).val())
    });

    let csrftoken = getCookie('csrftoken');
    let headers = new Headers();
    headers.append("X-CSRFToken", csrftoken);

    let url = baseUri + path
    let response = await fetch(url, {
        method: "POST",
        body: formData,
        headers: headers,
        redirect: 'follow'
    });
    if (response.ok) {
        window.location.reload()
    }
}

function createService() {
    let path = '/api/service/create/'
    requestOnCreate(path, '#serviceForm').then()
}

function createBonus() {
    let path = '/api/bonus/create/'
    requestOnCreate(path, '#bonusForm')
}

function createClient() {
    let path = '/api/client/create/'
    requestOnCreate(path, '#clientForm')
}

function createFine() {
    let path = '/api/fine/create/'
    requestOnCreate(path, '#fineForm')
}

function createInventory() {
    let path = '/api/inventory/create/'
    requestOnCreate(path, '#inventoryForm')
}

function createObjectType() {
    let path = '/api/object_type/create/'
    requestOnCreate(path, '#objectTypeForm')
}

async function modalServiceOrderUpdateOpen(event) {
    let pk = event.currentTarget.dataset.pk
    let pathname = window.location.pathname
    let btn = document.getElementById('unique')
    btn.setAttribute('data-pk', pk)
    let option = document.createElement('option')
    let select = document.getElementById('service')
    let amount = document.getElementById("amount")
    let rate = document.getElementById("rate")
    let csrftokens = getCookie('csrftoken');
    let url = `/api/update/service/${pk}`.replace(pathname, '')
    let response = await fetch(url, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftokens
        }
    })
    let answer = await response.json()
    option.value = answer["service"]['id']
    option.selected = true
    option.innerHTML = answer['service']['name']
    amount.value = answer['amount']
    rate.value = answer['rate']
    select.appendChild(option)
    let modal = document.getElementById('ServiceOrderUpdate');
    modal.style.display = "block"
    modal.style.background = 'rgba(0, 0 , 0, 0.2)'
    modal.focus()
}

async function modalServiceOrderUpdateClose() {
    let modal = document.getElementById('ServiceOrderUpdate');
    modal.style.display = "none"
}

async function updateServiceOrder(event) {
    let new_pk = event.currentTarget.dataset.pk
    let pathname = window.location.pathname
    let amount = document.getElementById("amount").value
    let rate = document.getElementById("rate").value
    let csrftokens = getCookie('csrftoken');
    let url = `/api/update/service/${new_pk}`.replace(pathname, '')
    let data = {"amount": amount, 'rate': rate};
    let response = await fetch(url, {
        method: "PUT",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftokens
        }

    })
    if (response.ok) {
        modalServiceOrderUpdateClose()
    }
}

async function modalServiceOrderDeleteOpen(event) {
    let modal = document.getElementById('ServiceOrderDelete');
    let pk = event.currentTarget.dataset.pk
    let info_div = document.getElementById('service-info')
    let text = event.currentTarget.dataset.nameText
    let p = document.createElement('p')
    p.innerText = text
    p.classList = ['text-center m-3']
    info_div.appendChild(p)
    let btn = document.getElementById('unique-delete')
    btn.setAttribute('data-pk', pk)
    modal.style.display = "block"
    modal.style.background = 'rgba(0, 0 , 0, 0.2)'
    modal.focus()
}

async function modalServiceOrderDeleteClose() {
    let modal = document.getElementById('ServiceOrderDelete');
    let info_div = document.getElementById('service-info')
    info_div.removeChild(info_div.children[0])
    modal.style.display = "none"
}

async function deleteServiceOrder(event) {
    let pk = event.target.dataset.pk
    let pathname = window.location.pathname
    let csrftokens = getCookie('csrftoken');
    let url = `/api/delete/service/${pk}`.replace(pathname, '')
    let response = await fetch(url, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftokens
        }
    })
    if (response.ok) {
        modalServiceOrderDeleteClose();
    }
}

async function modalInventoryOrderDeleteOpen(event) {
    let modal = document.getElementById('InventoryOrderDelete');
    let pk = event.currentTarget.dataset.pk
    let info_div = document.getElementById('inventory-info')
    let text = event.currentTarget.dataset.nameText
    let p = document.createElement('p')
    p.innerText = text
    p.classList = ['text-center m-3']
    info_div.appendChild(p)
    let btn = document.getElementById('inventory-delete')
    btn.setAttribute('data-pk', pk)
    modal.style.display = "block"
    modal.style.background = 'rgba(0, 0 , 0, 0.2)'
    modal.focus()
}

async function modalInventoryOrderDeleteClose() {
    let modal = document.getElementById('InventoryOrderDelete');
    let info_div = document.getElementById('inventory-info')
    info_div.removeChild(info_div.children[0])
    modal.style.display = "none"
}

async function deleteInventoryOrder(event) {
    let pk = event.currentTarget.dataset.pk
    let pathname = window.location.pathname
    let csrftokens = getCookie('csrftoken');
    let url = `/api/delete/inventory/${pk}`.replace(pathname, '')
    let response = await fetch(url, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftokens
        }
    })
    if (response.ok) {
        modalInventoryOrderDeleteClose();
    }
}
