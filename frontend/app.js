const API_URL = "http://127.0.0.1:8000";


/* ============================================================
   Check Backend Status
   ============================================================ */

async function checkStatus() {

    const status = document.getElementById("status");

    try {

        const response = await fetch(
            `${API_URL}/health`
        );

        const data = await response.json();

        if (data.status === "online") {

            status.textContent =
                "● LLM Online";

            status.style.background =
                "#166534";

        } else {

            status.textContent =
                "● Backend Online / LLM Offline";

            status.style.background =
                "#92400e";
        }

    } catch (error) {

        status.textContent =
            "● Backend Offline";

        status.style.background =
            "#991b1b";
    }
}


/* ============================================================
   Analyze Code
   ============================================================ */

async function analyzeCode() {

    const code =
        document.getElementById("code").value;

    const language =
        document.getElementById("language").value;

    const task =
        document.getElementById("task").value;

    const errorMessage =
        document.getElementById("error").value;

    const result =
        document.getElementById("result");

    const syntaxResult =
        document.getElementById("syntaxResult");

    const button =
        document.getElementById("analyzeBtn");


    if (!code.trim()) {

        alert("Please enter some code.");

        return;
    }


    button.disabled = true;

    button.textContent =
        "Analyzing...";


    result.innerHTML = `
        <div class="empty-state">
            <div class="icon">⏳</div>
            <h3>Analyzing your code...</h3>
            <p>The LLM is preparing the response.</p>
        </div>
    `;


    syntaxResult.classList.add(
        "hidden"
    );


    try {

        const response = await fetch(
            `${API_URL}/api/analyze`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    code: code,

                    language: language,

                    task: task,

                    error_message:
                        errorMessage

                })
            }
        );


        const data =
            await response.json();


        if (!data.success) {

            throw new Error(
                data.message ||
                "Analysis failed."
            );
        }


        /* ====================================================
           Syntax Result
           ==================================================== */

        if (data.syntax_check) {

            syntaxResult.classList.remove(
                "hidden"
            );


            if (data.syntax_check.valid) {

                syntaxResult.className =
                    "syntax-result syntax-success";

                syntaxResult.textContent =
                    "✓ " +
                    data.syntax_check.message;

            } else {

                syntaxResult.className =
                    "syntax-result syntax-error";

                syntaxResult.textContent =
                    "⚠ " +
                    data.syntax_check.message;
            }
        }


        /* ====================================================
           Display Answer
           ==================================================== */

        result.innerHTML = `
            <div class="result-content">
                ${escapeHtml(data.answer)}
            </div>
        `;

    }

    catch (error) {

        result.innerHTML = `
            <div class="syntax-result syntax-error">
                <strong>Error:</strong>
                ${escapeHtml(error.message)}
            </div>
        `;
    }

    finally {

        button.disabled = false;

        button.textContent =
            "Analyze Code";
    }
}


/* ============================================================
   Clear
   ============================================================ */

function clearAll() {

    document.getElementById(
        "code"
    ).value = "";

    document.getElementById(
        "error"
    ).value = "";


    document.getElementById(
        "result"
    ).innerHTML = `
        <div class="empty-state">
            <div class="icon">🤖</div>
            <h3>Ready to analyze your code</h3>
            <p>
                Enter your code and select an analysis mode.
            </p>
        </div>
    `;


    document.getElementById(
        "syntaxResult"
    ).classList.add("hidden");
}


/* ============================================================
   Copy Result
   ============================================================ */

async function copyResult() {

    const result =
        document.getElementById(
            "result"
        ).innerText;

    try {

        await navigator.clipboard.writeText(
            result
        );

        alert("Result copied!");

    } catch (error) {

        alert(
            "Could not copy the result."
        );
    }
}


/* ============================================================
   Escape HTML
   ============================================================ */

function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent =
        text;

    return div.innerHTML;
}


/* ============================================================
   Initialize
   ============================================================ */

checkStatus();

setInterval(
    checkStatus,
    10000
);
