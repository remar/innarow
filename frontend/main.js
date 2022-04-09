function createNewGame() {
    fetch("/api/games", {
        method: "POST"
    }).then(() => listGames());
}
function listGames() {
    fetch("/api/games").then(response => {
        if (response.ok) {
            response.json().then(gamesObject => {
                const gameList = document.getElementById("game_list");
                gameList.innerHTML = "";
                for (const element of gamesObject.games) {
                    const li = document.createElement("li");
                    const button = document.createElement("button");
                    button.innerHTML = element;
                    li.appendChild(button);
                    gameList.appendChild(li);
                }
            });
        }
    });
}
function handleCredentialResponse(response) {
    console.log(response.credential);
    fetch("/api/google-login", {
        method: "POST",
        body: response.credential
    }).then(response => console.log(response));
}
function getEmail() {
    return document.getElementById("show_email").innerHTML;
}
function setEmail(email) {
    document.getElementById("show_email").innerHTML = email;
}
function setEmailLoop() {
    if (!getEmail()) {
        fetch("/api/get-email").then(response => {
            if (response.ok) {
                response.text().then(email => setEmail(email));
            }
        });
        setTimeout(setEmailLoop, 1000);
    }
}

window.onload = setEmailLoop;
