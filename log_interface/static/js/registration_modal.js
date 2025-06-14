document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("register-modal");
    const openModalBtn = document.getElementById("open-modal");
    const closeModalBtn = document.getElementById("close-modal");

    const registerBtn = document.getElementById("register-btn");
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    function registerAccount(){
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        if (username === "" || password === ""){
            alert("Username and Password needs to be filled in!")
        }
        else{
            const requestData = {
                username: username,
                password: password,
            }

            try{
                fetch("/register",
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                })
                .then(response => {
                    return response.json().then(data => {
                        if (response.status === 200){
                            alert("Account created!")
                            usernameInput.value = ""
                            passwordInput.value = ""
                            adminCheckboxInput.value = false
                            closeModal()
                        } else if (response.status === 403){
                            alert(data.message)
                        } else if (response.status === 409){
                            alert("Account already exists with that username. Try log in!")
                        } else{
                            alert("Account could not be created ;(")
                        }
                    })
                })
                .catch(exception => {
                    console.error(exception)
                })
            }
            catch{
                alert("Error creating account.")
            }
        }
    }

    registerBtn.addEventListener("click", registerAccount)
    function openModal() {
        modal.style.display = "flex";
    }

    function closeModal() {
        modal.style.display = "none";
    }

    openModalBtn.addEventListener("click", openModal);

    closeModalBtn.addEventListener("click", closeModal);

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });
});