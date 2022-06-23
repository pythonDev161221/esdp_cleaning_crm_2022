async function make_request(url, method = 'GET') {
    let response = await fetch(url, {method})
    if (response.ok) {
        console.log('OK')
        return await response.json();
    } else {
        console.log('Not Successful')
        let error = new Error(response.statusText);
        error.response = response;
        throw error;
    }
}

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
    console.log(copyBtn);
    window.addEventListener('click', () => {
        const token = copyBtn.getAttribute('data-token');
        navigator.clipboard.writeText(token);
        copyBtn.textContent = 'Token скопирован';
    })
}

async function modalClientOpen() {
    let modal = document.getElementById('ClientModal');
    modal.style.display = "block"
    modal.style.background = 'rgba(0, 0 , 0, 0.2)'
    modal.focus()
}

async function modalClientClose() {
    let modal = document.getElementById('ClientModal');
    modal.style.display = "none"
}

async function createClient() {
    let pathname = window.location.pathname
    let first_name = document.getElementById("first_name").value;
    let last_name = document.getElementById("last_name").value;
    let phone = document.getElementById("phone").value;
    let organization = document.getElementById("organization").value;
    let csrftokens = getCookie('csrftoken');
    let url = "/api/client/create/".replace(pathname, '')
    let data = {"first_name": first_name, "last_name": last_name, "phone": phone, "organization": organization};
    let response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftokens
        }})
}

async function modalFineOpen() {
    let modal = document.getElementById('FineModal');
    modal.style.display = "block"
    modal.style.background = 'rgba(0, 0 , 0, 0.2)'
    modal.focus()
}

async function modalFineClose() {
    let modal = document.getElementById('FineModal');
    modal.style.display = "none"
}

async function createFine() {
    let pathname = window.location.pathname
    let category = document.getElementById("category").value;
    let fine = document.getElementById("fine").value;
    let criteria = document.getElementById("criteria").value;
    let value = document.getElementById("fine_value").value;
    let description = document.getElementById("description").value;
    let csrftoken = getCookie('csrftoken');
    let url =  "/api/fine/create/".replace(pathname, '')
    let data = {"category": category, "fine": fine, "criteria": criteria, "value": value, "description": description};
    let response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    if (response.ok) {
        modalFineClose()}
}

async function modalBonusOpen() {
    let modal = document.getElementById('BonusModal');
    modal.style.display = "block"
    modal.style.background = 'rgba(0, 0 , 0, 0.2)'
    modal.focus()
}

async function modalBonusClose() {
    let modal = document.getElementById('BonusModal');
    modal.style.display = "none"
}

async function createBonus() {
    let pathname = window.location.pathname
    let bonus = document.getElementById("bonus").value;
    let bonus_value = document.getElementById("bonus_value").value;
    let csrftoken = getCookie('csrftoken');
    let url =  "/api/bonus/create/".replace(pathname, '')
    let data = {"bonus": bonus, "value": bonus_value};
    let response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    if (response.ok) {
        modalBonusClose()}
}

async function modalInventoryOpen() {
    let modal = document.getElementById('InventoryModal');
    modal.style.display = "block"
    modal.style.background = 'rgba(0, 0 , 0, 0.2)'
    modal.focus()
}

async function modalInventoryClose() {
    let modal = document.getElementById('InventoryModal');
    modal.style.display = "none"
}

async function createInventory() {
    let pathname = window.location.pathname
    let inventory = document.getElementById("inventory_name").value;
    let inventory_description = document.getElementById("inventory_description").value;
    let csrftoken = getCookie('csrftoken');
    let url =  "/api/inventory/create/".replace(pathname, '')
    let data = {"name": inventory, "description": inventory_description};
    let response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    if (response.ok) {
        modalInventoryClose()}
}

async function modalObjectTypeOpen() {
    let modal = document.getElementById('ObjectTypeModal');
    modal.style.display = "block"
    modal.style.background = 'rgba(0, 0 , 0, 0.2)'
    modal.focus()
}

async function modalObjectTypeClose() {
    let modal = document.getElementById('ObjectTypeModal');
    modal.style.display = "none"
}

async function createObjectType() {
    let pathname = window.location.pathname
    let object_type_name = document.getElementById("object_type_name").value;
    let csrftoken = getCookie('csrftoken');
    let url = "/api/object_type/create/".replace(pathname, '')
    let data = {"name": object_type_name};
    let response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    if (response.ok) {
        modalObjectTypeClose()}
}


