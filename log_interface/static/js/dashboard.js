let targetProjectId = ""

function toggleProjectLogs(projectId) {
    const logsList = document.getElementById(`logs-list-${projectId}`);
    const expandIcon = document.getElementById(`expand-icon-${projectId}`);
    if (logsList.style.display === "none") {
        logsList.style.display = "flex";
        expandIcon.textContent = "-";
    } else {
        logsList.style.display = "none";
        expandIcon.textContent = "+";
    }
}

function toggleLogMessage(logId) {
    const logDetails = document.getElementById(`log-details-${logId}`);
    const expandIcon = document.getElementById(`expand-log-icon-${logId}`);
    if (logDetails.style.display === "none") {
        logDetails.style.display = "block";
        expandIcon.textContent = "-";
    } else {
        logDetails.style.display = "none";
        expandIcon.textContent = "+";
    }
}

function onCreateLogMessage(projectId){
    targetProjectId = projectId
}

async function deleteLog(logId) {
    const userConfirmed = confirm("Are you sure you want to delete this log?");
    
    if (userConfirmed) {
        fetch(`http://127.0.0.1:5000/delete_log/${logId}`, {
            method: "DELETE"
        })
        .then(response => {
            if (response.status == 200){
                alert("Log Deleted.")
                window.location.href = '/dashboard'
            } else{
                alert("Error deleting log.")
            }
        })
    } else {
        alert("Deletion canceled.");
    }
}

async function deleteProject(projectId){
    const userConfirmed = confirm("Are you sure you want to delete this Project? \nThis will delete all associated logs in a cascading effect.");
    
    if (userConfirmed) {
        fetch(`http://127.0.0.1:5000/delete_project/${projectId}`, {
            method: "DELETE"
        })
        .then(response => {
            if (response.status == 200){
                alert("Project Deleted.")
                window.location.href = '/dashboard'
            } else{
                alert("Error deleting Project.")
            }
        })
    } else {
        alert("Deletion canceled.");
    }
}

async function logout() {
    const userConfirmed = confirm("Are you sure you want to logout?");
    
    if (userConfirmed) {
        try{
            fetch("http://127.0.0.1:5000/logout",
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.status === 200){
                    window.location.href = '/'
                } else{
                    alert("Unable to logout")
                }
            })
            .catch(exception => {
                console.error(exception)
            })
        }
        catch{
            alert("Unable to logout")
        }
    }
}