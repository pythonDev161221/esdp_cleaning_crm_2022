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
    console.log('aaa')
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
        }
    })
    console.log(response.status)
}