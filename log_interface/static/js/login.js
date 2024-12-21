const inputBox = document.getElementById('login-entry');
const passwordInput = document.getElementById('password-input');
const usernameInput = document.getElementById('username-input')
const submitButton = document.getElementById('submit-button');

async function checkPassword() {
    const requestData = {
        username: usernameInput.value.trim(),
        password: passwordInput.value.trim()
    }
    try{
        fetch("/login",
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            if (response.status === 200){
                inputBox.style.borderColor = 'green';
                window.location.href = '/dashboard'
            } else{
                inputBox.style.borderColor = 'red';
            }
        })
        .catch(exception => {
            console.error(exception)
            inputBox.style.borderColor = 'red';
        })
    }
    catch{
        inputBox.style.borderColor = 'red';
    }
}

passwordInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        checkPassword();
    } else if (event.key === 'Backspace') {
        inputBox.style.borderColor = 'white';
    }
});

submitButton.addEventListener('click', checkPassword);