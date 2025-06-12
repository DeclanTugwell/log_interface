let targetProjectId = "";
const socket = io();
const widgetState = {
    projects: {},
    users: {},
    sessions: {},
    logs: {},
};

// Initialize widget states upon loading the page
function initializeWidgetStates(projects) {
    console.log(projects)
    projects.forEach((project) => {
        widgetState.projects[project.project_id] = false; // Collapsed
        project.project_users.forEach((user) => {
            widgetState.users[user.user_id] = false; // Collapsed
            user.session_list.forEach((session) => {
                widgetState.sessions[session.session_id] = false; // Collapsed
                session.log_list.forEach((log) => {
                    widgetState.logs[log.log_id] = false; // Collapsed
                });
            });
        });
    });
}

// Helper function to toggle visibility
function toggleVisibility(elementId, isExpanded, expandIconId) {
    const element = document.getElementById(elementId);
    const expandIcon = document.getElementById(expandIconId);

    if (!element || !expandIcon) return;

    if (isExpanded) {
        element.style.display = "flex";
        expandIcon.textContent = "-";
    } else {
        element.style.display = "none";
        expandIcon.textContent = "+";
    }
}

// Toggle project users
function toggleProjectUsers(projectId) {
    widgetState.projects[projectId] = !widgetState.projects[projectId];
    toggleVisibility(
        `project-users-${projectId}`,
        widgetState.projects[projectId],
        `expand-icon-${projectId}`
    );
}

// Toggle user sessions
function toggleUserSessions(userId) {
    widgetState.users[userId] = !widgetState.users[userId];
    toggleVisibility(
        `user-sessions-${userId}`,
        widgetState.users[userId],
        `expand-user-icon-${userId}`
    );
}

// Toggle session logs
function toggleSessionLogs(sessionId) {
    widgetState.sessions[sessionId] = !widgetState.sessions[sessionId];
    toggleVisibility(
        `session-logs-${sessionId}`,
        widgetState.sessions[sessionId],
        `expand-session-icon-${sessionId}`
    );
}

// Toggle log message details
function toggleLogMessage(logId) {
    widgetState.logs[logId] = !widgetState.logs[logId];
    toggleVisibility(
        `log-details-${logId}`,
        widgetState.logs[logId],
        `expand-log-icon-${logId}`
    );
}

// Fetch and update the projects list
socket.on("update_projects", () => {
    try {
        fetch("/get_projects", {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        })
            .then((response) => {
                if (response.status === 200) {
                    return response.json();
                } else {
                    alert("Issue fetching projects");
                    throw new Error("Project fetch failed");
                }
            })
            .then((data) => {
                updateProjectsList(data.projects);
            })
            .catch((exception) => {
                console.error(exception);
            });
    } catch {
        alert("Unable to fetch projects");
    }
});

function updateProjectsList(projects) {
    // Step 1: Capture the current widget states
    const widgetStates = {
        projectUsers: {},
        userSessions: {},
        sessionLogs: {},
    };

    document.querySelectorAll(".project-users-list").forEach((el) => {
        const projectId = el.id.split("-")[2]; // Extract project_id
        widgetStates.projectUsers[projectId] = el.style.display !== "none";
    });

    document.querySelectorAll(".user-sessions-list").forEach((el) => {
        const userId = el.id.split("-")[2]; // Extract user_id
        widgetStates.userSessions[userId] = el.style.display !== "none";
    });

    document.querySelectorAll(".session-logs-list").forEach((el) => {
        const sessionId = el.id.split("-")[2]; // Extract session_id
        widgetStates.sessionLogs[sessionId] = el.style.display !== "none";
    });

    // Step 2: Clear and rebuild the DOM
    const projectsContainer = document.querySelector(".projects-list");
    projectsContainer.innerHTML = ""; // Clear the current projects list

    projects.forEach((project) => {
        const projectWidget = document.createElement("div");
        projectWidget.classList.add("project-widget");

        projectWidget.innerHTML = `
            <div class="project-header" onclick="toggleProjectUsers('${project.project_id}')">
                <span class="project-name">(${project.project_id}) ${project.project_name}</span>
                <span class="expand-icon" id="expand-icon-${project.project_id}">+</span>
            </div>
            <div class="project-users-list" id="project-users-${project.project_id}" style="display: none;">
                ${project.project_users
                    .map(
                        (user) => `
                    <div class="project-user-widget">
                        <div class="project-user-header" onclick="toggleUserSessions('${user.user_id}')">
                            <span>${user.hardware_id}</span>
                            <div class="user-log-summary">
                                <span class="log-type-info"><b>Info: ${user.info_count}</b></span>
                                <span class="log-type-event"><b>Events: ${user.event_count}</b></span>
                                <span class="log-type-warning"><b>Warnings: ${user.warning_count}</b></span>
                                <span class="log-type-error"><b>Errors: ${user.error_count}</b></span>
                            </div>
                            <span class="expand-icon" id="expand-user-icon-${user.user_id}">+</span>
                        </div>
                        <div class="user-sessions-list" id="user-sessions-${user.user_id}" style="display: none;">
                            ${user.session_list
                                .map(
                                    (session) => `
                                <div class="user-session-widget">
                                    <div class="user-session-header" onclick="toggleSessionLogs('${session.session_id}')">
                                        <span>${session.timestamp_str}</span>
                                        <div class="session-log-summary">
                                            <span class="log-type-info"><b>Info: ${session.info_count}</b></span>
                                            <span class="log-type-event"><b>Events: ${session.event_count}</b></span>
                                            <span class="log-type-warning"><b>Warnings: ${session.warning_count}</b></span>
                                            <span class="log-type-error"><b>Errors: ${session.error_count}</b></span>
                                        </div>
                                        <span class="expand-icon" id="expand-session-icon-${session.session_id}">+</span>
                                    </div>
                                    <div class="session-logs-list" id="session-logs-${session.session_id}" style="display: none;">
                                        ${session.log_list
                                            .map(
                                                (log) => `
                                            <div class="log-widget">
                                                <div class="log-header" onclick="toggleLogMessage('${log.log_id}')">
                                                    <span class="log-timestamp">${log.timestamp}</span>
                                                    <span class="log-type log-type-${log.log_type.toLowerCase()}">${log.log_type.toLowerCase()}</span>
                                                    <span class="expand-icon" id="expand-log-icon-${log.log_id}">+</span>
                                                </div>
                                                <div class="log-details" id="log-details-${log.log_id}" style="display: none;">
                                                    <div class="log-message-container">
                                                        <p class="log-message">${log.message}</p>
                                                    </div>
                                                    <div class="delete-log-container">
                                                        <button class="delete-log-btn delete-btn" onclick="deleteLog('${log.log_id}')">Delete Log</button>
                                                    </div>
                                                </div>
                                            </div>
                                        `
                                            )
                                            .join("")}
                                        <div class="delete-session-container">
                                            <button class="delete-session-btn delete-btn" onclick="deleteSession('${session.session_id}')">Delete Session</button>
                                        </div>
                                    </div>
                                </div>
                            `
                                )
                                .join("")}
                            <button class="delete-project-user-btn delete-btn" onclick="deleteProjectUser('${user.user_id}')">Delete Project User</button>
                        </div>
                    </div>
                `
                    )
                    .join("")}
                <button class="delete-project-btn delete-btn" onclick="deleteProject('${project.project_id}')">Delete Project</button>
            </div>
        `;
        projectsContainer.appendChild(projectWidget);
    });

    // Step 3: Restore the widget states
    Object.keys(widgetStates.projectUsers).forEach((projectId) => {
        const el = document.getElementById(`project-users-${projectId}`);
        if (el) {
            el.style.display = widgetStates.projectUsers[projectId] ? "flex" : "none";
        }
    });

    Object.keys(widgetStates.userSessions).forEach((userId) => {
        const el = document.getElementById(`user-sessions-${userId}`);
        if (el) {
            el.style.display = widgetStates.userSessions[userId] ? "flex" : "none";
        }
    });

    Object.keys(widgetStates.sessionLogs).forEach((sessionId) => {
        const el = document.getElementById(`session-logs-${sessionId}`);
        if (el) {
            el.style.display = widgetStates.sessionLogs[sessionId] ? "flex" : "none";
        }
    });
}
async function deleteLog(logId) {
    const userConfirmed = confirm("Are you sure you want to delete this log?");
    if (userConfirmed) {
        fetch(`/delete_log/${logId}`, {
            method: "DELETE"
        })
        .then(response => {
            if (response.status === 200) {
                alert("Log deleted.");
            } else {
                alert("Error deleting log.");
            }
        });
    } else {
        alert("Deletion canceled.");
    }
}

async function deleteSession(sessionId) {
    const userConfirmed = confirm("Are you sure you want to delete this session? \nThis will delete all associated logs in a cascading effect.");
    if (userConfirmed) {
        fetch(`/delete_session/${sessionId}`, {
            method: "DELETE"
        })
        .then(response => {
            if (response.status === 200) {
                alert("Session deleted.");
            } else {
                alert("Error deleting session.");
            }
        });
    } else {
        alert("Deletion canceled.");
    }
}

async function deleteProjectUser(userId) {
    const userConfirmed = confirm("Are you sure you want to delete this project user? \nThis will delete all associated sessions and logs in a cascading effect.");
    if (userConfirmed) {
        fetch(`/delete_project_user/${userId}`, {
            method: "DELETE"
        })
        .then(response => {
            if (response.status === 200) {
                alert("Project user deleted.");
            } else {
                alert("Error deleting project user.");
            }
        });
    } else {
        alert("Deletion canceled.");
    }
}

async function deleteProject(projectId) {
    const userConfirmed = confirm("Are you sure you want to delete this Project? \nThis will delete all associated logs, sessions, and users in a cascading effect.");
    if (userConfirmed) {
        fetch(`/delete_project/${projectId}`, {
            method: "DELETE"
        })
        .then(response => {
            if (response.status === 200) {
                alert("Project deleted.");
            } else {
                alert("Error deleting Project.");
            }
        });
    } else {
        alert("Deletion canceled.");
    }
}

async function logout() {
    const userConfirmed = confirm("Are you sure you want to logout?");
    if (userConfirmed) {
        try {
            fetch("/logout", {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.status === 200) {
                    window.location.href = '/';
                } else {
                    alert("Unable to logout");
                }
            })
            .catch(exception => {
                console.error(exception);
            });
        } catch {
            alert("Unable to logout");
        }
    }
}