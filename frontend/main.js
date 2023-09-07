let currentGame = -1;
let board = [];

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
        if (response.ok) {
            response.json().then(game => {
                let current = 1;
                clearBoard();
                for (const move of game.moves) {
                    const el = renderElement(current);
                    board[move[0]][move[1]].innerHTML = el;
                    board[move[0]][move[1]].className = el;
                    current = current % 2 + 1;
                }
                renderedBoard = game.player1 + " vs " + game.player2 + "\n";
		renderedBoard += "Winner: " + showWinner(game) + "\n";
                document.getElementById("show_game").innerHTML = renderedBoard;
            });
        }
    });
}

function showWinner(game) {
    if(game.winner === null) {
	return "undecided";
    }
    return game.winner + " (" + (game.winner === "x" ? game.player1 : game.player2) + ")";
}

function clearBoard() {
    for(let y = 0;y < 15;y++) {
        for(let x = 0;x < 15;x++) {
            board[x][y].innerHTML = "";
        }
    }
}


function joinGame(id) {
    fetch(`/api/games/${id}`, {
        method: "PATCH"
    });
}

function move(x, y) {
    if (currentGame == -1) {
        return;
    }

    fetch(`/api/games/${currentGame}`, {
        method: "POST",
        body: JSON.stringify({"x": x, "y": y})
    }).then(response => {
        if (response.ok) {
            showGame(currentGame);
        }
    });
}

function renderElement(element) {
    if (element === 0) {
        return ".";
    } else if (element == 1) {
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

window.onload = () => {
    setEmailLoop();
    document.getElementById("board").appendChild(clickableGrid(15, 15, (el, r, c) => {
        console.log("row: " + r + ", col: " + c);
        move(c, r);
    }));
}

function clickableGrid(rows, cols, callback) {
    for (let y = 0; y < 15; y++) {
        board.push(Array.from({ length: 15 }, () => 0));
    }

    var grid = document.createElement('table');
    grid.className = 'grid';
    for (var r = 0; r < rows; ++r) {
        var tr = grid.appendChild(document.createElement('tr'));
        for (var c = 0; c < cols; ++c) {
            var cell = tr.appendChild(document.createElement('td'));
            cell.addEventListener('click', (function (el, r, c) {
                return function () {
                    callback(el, r, c);
                }
            })(cell, r, c), false);
            board[c][r] = cell;
        }
    }
    return grid;
}
