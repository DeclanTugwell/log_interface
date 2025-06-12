document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("account-management-modal");
    const openModalBtn = document.getElementById("open-admin-modal");
    const closeModalBtn = document.getElementById("close-admin-modal");

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

function confirmDelete(accountId) {
    const userConfirmed = confirm("Are you sure you want to delete this account?");
    
    if (userConfirmed) {
        fetch(`/delete_account/${accountId}`, {
            method: "DELETE"
        })
        .then(response => {
            if (response.status == 200){
                alert("Account Deleted.")
                window.location.href = '/dashboard'
            } else if(response.status == 403){
                alert("Can't delete currently logged in account.")
            }
            else{
                alert("Error deleting account.")
            }
        })
    } else {
        alert("Deletion canceled.");
    }
}

function downloadDatabase() {
    fetch('/download_database')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.blob();
      })
      .then(blob => {
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'database.db';

        document.body.appendChild(a);
        a.click();

        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      })
      .catch(error => {
        console.error('Error downloading database:', error);
      });
  }