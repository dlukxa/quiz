document.addEventListener("DOMContentLoaded", function () {
    const app = document.getElementById("app");
    const welcome = document.querySelector(".welcome");
    const nameInput = document.getElementById("name");
    const startButton = document.getElementById("startButton");
    const questionContainer = document.getElementById("questionContainer");
    const resultDiv = document.getElementById("result");
    const scoreboardDiv = document.getElementById("scoreboard");
    const newGameButton = document.getElementById("newGameButton");
    const timerDiv = document.getElementById("timer");

    const questionSets = [
        [["How many e are in the periodic table?"], ["A. 116", "B. 117", "C. 118", "D. 119"], "C"],
        [["Which animal lays the largest eggs?"], ["A. Whale", "B. Crocodile", "C. Elephant", "D. Ostrich"], "D"],
        // ... Add more question sets here ...
    ];    
    let currentQuestion = 0;
    let score = 0;
    let timerValue = 7;
    let countdownInterval;

    startButton.addEventListener("click", startQuiz);
    newGameButton.addEventListener("click", newGame);

    function startQuiz() {
        const name = nameInput.value.trim();
        if (name === "") return;

        welcome.style.display = "none";
        nameInput.style.display = "none";
        startButton.style.display = "none";
        newGameButton.disabled = true;

        shuffleArray(questionSets);
        questionSets = questionSets.slice(0, 8);
        currentQuestion = 0;
        score = 0;
        updateQuestion();
    }

    function updateQuestion() {
        if (currentQuestion < questionSets.length) {
            const questionSet = questionSets[currentQuestion];
            const questionText = questionSet[0][0];
            const answers = questionSet[1];

            questionContainer.innerHTML = `<h2>${questionText}</h2>`;

            for (let i = 0; i < answers.length; i++) {
                questionContainer.innerHTML += `<button class="answerButton">${answers[i]}</button>`;
            }

            startTimer();
            currentQuestion++;
        } else {
            showResult();
        }
    }

    function startTimer() {
        timerValue = 7;
        timerDiv.textContent = `Time Remaining: ${timerValue} seconds`;
        countdownInterval = setInterval(updateTimer, 1000);
    }

    function updateTimer() {
        if (timerValue >= 0) {
            timerDiv.textContent = `Time Remaining: ${timerValue} seconds`;
            timerValue--;
        } else {
            clearInterval(countdownInterval);
            checkAnswer(-1);
        }
    }

    function checkAnswer(selectedIdx) {
        clearInterval(countdownInterval);
        const correctAnswer = questionSets[currentQuestion - 1][2];
        if (selectedIdx === correctAnswer.charCodeAt(0) - "A".charCodeAt(0)) {
            score++;
        }
        questionContainer.innerHTML = "";
        updateQuestion();
    }

    function showResult() {
        const percentageCorrect = (score * 100) / questionSets.length;
        resultDiv.textContent = `Congratulations ${nameInput.value}, your marks for the Quiz is ${percentageCorrect.toFixed(2)}%.`;

        showScoreboard();

        newGameButton.disabled = false;
    }

    function showScoreboard() {
        // Implement your scoreboard logic here
    }

    function newGame() {
        nameInput.value = "";
        welcome.style.display = "block";
        nameInput.style.display = "block";
        startButton.style.display = "block";
        questionContainer.innerHTML = "";
        resultDiv.textContent = "";
        scoreboardDiv.textContent = "";
        timerDiv.textContent = "";
        newGameButton.disabled = true;
    }

    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }
});
