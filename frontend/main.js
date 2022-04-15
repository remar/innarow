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
                for (const id of gamesObject.games) {
                    const li = document.createElement("li");
                    const button = document.createElement("button");
                    button.innerHTML = id;
                    button.onclick = () => showGame(id);
                    li.appendChild(button);
                    gameList.appendChild(li);
                }
            });
        }
    });
}

function showGame(id) {
    fetch(`/api/games/${id}`).then(response => {
        if(response.ok) {
            response.json().then(game => {
                const board = []
                for(let y = 0;y < 15;y++) {
                    board.push(Array.from({length: 15}, () => 0));
                }
                let current = 1;
                for(const move of game.moves) {
                    board[move[1]][move[0]] = current;
                    current = current % 2 + 1;
                }
                renderedBoard = board.map(line => line.map(element => renderElement(element)).join(" ")).join("\n");
                console.log(renderedBoard);
                document.getElementById("show_game").innerHTML = renderedBoard;
            });
        }
    });
}

function renderElement(element) {
    if(element === 0) {
        return ".";
    } else if(element == 1) {
        return "X";
    } else {
        return "O";
    }
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
