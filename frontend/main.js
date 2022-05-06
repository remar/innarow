let currentGame = -1;

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
                    li.appendChild(createButton(id, () => showGame(id)));
                    li.appendChild(createButton("Join", () => joinGame(id)));
                    gameList.appendChild(li);
                }
            });
        }
    });
}

function createButton(text, callback) {
    const button = document.createElement("button");
    button.innerHTML = text;
    button.onclick = callback;
    return button;
}

function showGame(id) {
    currentGame = id;
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
                renderedBoard = game.player1 + " vs " + game.player2 + "\n" +
                    "                     1 1 1 1 1 1\n" +
                    "   1 2 3 4 5 6 7 8 9 0 1 2 3 4 5\n" +
                    board.map((line, index) => `${index < 9 ? " ":""}${index + 1} ` + line.map(element => renderElement(element)).join(" ")).join("\n");
                console.log(renderedBoard);
                document.getElementById("show_game").innerHTML = renderedBoard;
            });
        }
    });
}

function joinGame(id) {
    fetch(`/api/games/${id}`, {
        method: "PATCH"
    });
}

function doMove() {
    if(currentGame == -1) {
        return;
    }

    fetch(`/api/games/${currentGame}`, {
        method: "POST",
        body: JSON.stringify({
            "x": parseInt(document.getElementById("x").value) - 1,
            "y": parseInt(document.getElementById("y").value) - 1
        })
    }).then(() => showGame(currentGame));
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
