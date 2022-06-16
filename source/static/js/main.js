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

const copyBtn = document.getElementById('copy-btn');
console.log(copyBtn);
window.addEventListener('click', () => {
    const token = copyBtn.getAttribute('data-token');
    navigator.clipboard.writeText(token);
    copyBtn.textContent = 'Token скопирован';
})