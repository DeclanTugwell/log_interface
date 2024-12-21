document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("project-modal");
    const openModalBtn = document.getElementById("project-open-modal");
    const closeModalBtn = document.getElementById("project-close-modal");
    const createProjBtn = document.getElementById("create-btn");
    const projNameInput = document.getElementById("project-name");
    const projectIdLabel = document.getElementById("project-id");
    const projectEndpointLabel = document.getElementById("endpoint-url");

    function openModal() {
        modal.style.display = "flex"; 
    }

    function closeModal() {
        modal.style.display = "none";
    }

    function createProject(){
        const projName =  projNameInput.value.trim()
        if (projName === ""){
            alert("Please enter a name for the project.")
        }
        else{
            const requestData = {
                projectName: projName
            }

            try{
                fetch("http://127.0.0.1:5000/create_project",
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                })
                .then(response => {
                    if (response.status === 200) {
                        alert("Project created, please refresh the page to view the project.")
                        return response.json();
                    } else if (response.status === 409) {
                        alert("Project name taken. Try a different name.");
                        throw new Error("Project name conflict");
                    } else {
                        alert("Project could not be created ;(");
                        throw new Error("Project creation failed");
                    }
                })
                .then(data => {
                    const projectId = data.body;
                    projectIdLabel.innerHTML = `<b>Project ID:</b> ${projectId}`
                    projectEndpointLabel.innerHTML = `<b>Endpoint:</b> http://127.0.0.1:5000/log/${projectId}`
                })
                .catch(exception => {
                    console.error(exception)
                })
            }
            catch{
                alert("Error creating project")
            }
        }
    }

    openModalBtn.addEventListener("click", openModal);

    closeModalBtn.addEventListener("click", closeModal);

    createProjBtn.addEventListener("click", createProject);

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });
});