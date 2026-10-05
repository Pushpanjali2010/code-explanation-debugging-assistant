from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import ast

from rag import retrieve_context
from prompts import build_prompt


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="AI Code Explanation and Debugging Assistant",
    description="LLM-powered code analysis assistant",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Configuration
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


# ============================================================
# Request Model
# ============================================================

class CodeRequest(BaseModel):
    code: str
    language: str = "Python"
    task: str = "Explain Code"
    error_message: str = ""


# ============================================================
# Health Check
# ============================================================

@app.get("/")
def home():
    return {
        "message": "AI Code Explanation and Debugging Assistant is running!"
    }


@app.get("/health")
def health():
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )

        if response.status_code == 200:
            return {
                "status": "online",
                "llm": MODEL_NAME
            }

        return {
            "status": "backend_online",
            "llm": "Ollama not responding"
        }

    except Exception:
        return {
            "status": "backend_online",
            "llm": "Ollama is not running"
        }


# ============================================================
# Python Syntax Analysis
# ============================================================

def check_python_syntax(code):

    try:
        ast.parse(code)

        return {
            "valid": True,
            "message": "No Python syntax errors detected."
        }

    except SyntaxError as error:

        return {
            "valid": False,
            "message": (
                f"Syntax Error at line {error.lineno}: "
                f"{error.msg}"
            )
        }

    except Exception as error:

        return {
            "valid": False,
            "message": str(error)
        }


# ============================================================
# Call Ollama
# ============================================================

def call_ollama(prompt):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_ctx": 4096
        }
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "The model did not return a response."
        )

    except requests.exceptions.ConnectionError:

        return (
            "ERROR: Ollama is not running.\n\n"
            "Please start Ollama and make sure the model "
            f"'{MODEL_NAME}' is installed."
        )

    except requests.exceptions.Timeout:

        return (
            "ERROR: The LLM took too long to respond. "
            "Try using a smaller code snippet."
        )

    except Exception as error:

        return f"ERROR while communicating with LLM: {str(error)}"


# ============================================================
# Main Analysis Endpoint
# ============================================================

@app.post("/api/analyze")
def analyze_code(request: CodeRequest):

    if not request.code.strip():

        return {
            "success": False,
            "message": "Please enter some code."
        }

    # --------------------------------------------------------
    # Python syntax check
    # --------------------------------------------------------

    syntax_result = None

    if request.language.lower() == "python":

        syntax_result = check_python_syntax(request.code)

    # --------------------------------------------------------
    # Retrieve relevant programming knowledge
    # --------------------------------------------------------

    context = retrieve_context(
        request.code,
        request.task
    )

    # --------------------------------------------------------
    # Build LLM prompt
    # --------------------------------------------------------

    prompt = build_prompt(
        task=request.task,
        language=request.language,
        code=request.code,
        error_message=request.error_message,
        context=context
    )

    # --------------------------------------------------------
    # Generate answer
    # --------------------------------------------------------

    answer = call_ollama(prompt)

    return {
        "success": True,
        "task": request.task,
        "language": request.language,
        "syntax_check": syntax_result,
        "retrieved_context": context,
        "answer": answer
    }