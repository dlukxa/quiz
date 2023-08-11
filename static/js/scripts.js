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

    let questionSets = {{ question_sets | tojson | safe }};
    
    const progressContainer = document.getElementById("progressContainer");
    const progressBars = [];

    let currentQuestion = 0;
    let score = 0;
    let timerValue = 10;
    let countdownInterval;

    startButton.addEventListener("click", startQuiz);
    newGameButton.addEventListener("click", newGame);

    function startQuiz() {
        const name = nameInput.value.trim();
        if (name === "") return;

        welcome.style.display = "none";
        nameInput.style.display = "none";
        startButton.style.display = "none";
        newGameButton.style.display = "none";

        questionSets = questionSets.slice(0, 7);
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
                const answerButton = document.createElement("button");
                answerButton.classList.add("answerButton");
                answerButton.textContent = answers[i];
                answerButton.addEventListener("click", () => checkAnswer(i));
                questionContainer.appendChild(answerButton);
            }
            // Create a progress bar for the current question
            const progressBar = document.createElement("div");
            progressBar.classList.add("progressBar");
            progressContainer.appendChild(progressBar);
            progressBars.push(progressBar); // Store the progress bar

            startTimer();
            currentQuestion++;
        } else {
            showResult();
        }
    }

    function startTimer() {
        timerValue = 10;
        timerDiv.textContent = `Time Remaining: ${timerValue} seconds`;
        countdownInterval = setInterval(updateTimer, 1000);
    }

    function updateTimer() {
        if (timerValue >= 0) {
            timerDiv.textContent = `Time Remaining: ${timerValue} seconds`;
            timerValue--;

            if (timerValue < 4 && timerValue >= 0) {
                startPulsing();
            } else {
                stopPulsing();
            }
        } else {
            clearInterval(countdownInterval);
            checkAnswer(-1);
        }
    }

    let pulsingInterval;

    function startPulsing() {
        document.body.classList.add('pulsing-background');
    }

    function stopPulsing() {
        document.body.classList.remove('pulsing-background');
    }


    function checkAnswer(selectedIdx) {
        clearInterval(countdownInterval);
        const correctAnswer = questionSets[currentQuestion - 1][2];
        const progressBar = progressBars[currentQuestion - 1]; // Get the corresponding progress bar

        if (selectedIdx === correctAnswer.charCodeAt(0) - "A".charCodeAt(0)) {
            score++;
            progressBar.classList.add("correct");
        } else {
            progressBar.classList.add("wrong");
        }

        questionContainer.innerHTML = "";
        updateQuestion();
    }

    function showResult() {
        const percentageCorrect = (score * 100) / questionSets.length;
        resultDiv.textContent = `Congratulations ${nameInput.value}, your marks for the Quiz is ${percentageCorrect.toFixed(2)}%.`;

        showScoreboard();

        newGameButton.style.display = "";

    }

    function showScoreboard() {
        // Implement your scoreboard logic here
    }

    function newGame() {
    fetch('/get_new_questions')
        .then(response => response.json())
        .then(newQuestions => {
            console.log('Received new questions:', newQuestions); // Debugging line

            // Reset the UI, including progress bars
            nameInput.value             = "";
            welcome.style.display       = "block";
            nameInput.style.display     = "block";
            startButton.style.display   = "block";
            questionContainer.innerHTML = "";
            resultDiv.textContent       = "";
            scoreboardDiv.textContent   = "";
            timerDiv.textContent        = "";
            newGameButton.style.display = "none";

            // Remove existing progress bars from the DOM
            while (progressContainer.firstChild) {
                progressContainer.removeChild(progressContainer.firstChild);
            }

            // Reset the progressBars array
            progressBars.length = 0;

            // Update questionSets with newQuestions
            questionSets = newQuestions;

            // Start the new quiz
            startQuiz();
        })
        .catch(error => console.error('Error:', error));
    }

    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }
});
