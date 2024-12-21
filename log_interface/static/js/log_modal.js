document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("log-modal");
    const closeModalBtn = document.getElementById("log-close-modal");
    const createLogBtn = document.getElementById("create-log-btn");
    const logMessageInput = document.getElementById("log-message");
    const logTypeSelection = document.getElementById("log-type");

    function openModal() {
        modal.style.display = "flex";
    }

    function closeModal() {
        modal.style.display = "none";
    }

    function createLog(){
        console.log(targetProjectId)
        const logMsg =  logMessageInput.value.trim()
        const logType = logTypeSelection.value
        if (logMsg === "" || logType === null){
            alert("Please enter a log message and type")
        }
        else{
            const requestData = {
                message: logMsg,
                logType: logType,
                timestamp: "",
                projectId: targetProjectId
            }

            try{
                fetch("/create_log",
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                })
                .then(response => {
                    if (response.status === 200) {
                        alert("Log Added.")
                        window.location.href = '/dashboard'
                        return response.json();
                    } else {
                        alert("Log could not be created ;(");
                    }
                })
                .catch(exception => {
                    console.error(exception)
                })
            }
            catch{
                alert("Error creating log")
            }
        }
    }

    const logOpenButtons = document.querySelectorAll(".log-open-modal");
    logOpenButtons.forEach(button => {
        button.addEventListener("click", openModal);
    });

    closeModalBtn.addEventListener("click", closeModal);

    createLogBtn.addEventListener("click", createLog);

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });
});