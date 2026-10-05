# ============================================================
# Prompt Builder
# ============================================================

def build_prompt(
    task,
    language,
    code,
    error_message,
    context
):

    base_instruction = """
You are an expert programming tutor and debugging assistant.

Your job is to help students understand programming concepts,
identify bugs, improve code quality, and learn good programming
practices.

Do NOT blindly assume that the code is wrong.

When explaining code:
- Use simple language.
- Explain the important parts clearly.
- Give examples where useful.
- Do not unnecessarily complicate the answer.

When debugging:
- Identify the likely problem.
- Explain WHY the problem occurs.
- Provide the corrected code.
- Mention edge cases.

When discussing complexity:
- Clearly state time complexity.
- Clearly state space complexity.
- Explain why.

Do not invent errors that are not present in the code.
"""


    task_instruction = ""


    # ========================================================
    # Task-specific Instructions
    # ========================================================

    if task == "Explain Code":

        task_instruction = """
Explain the provided code.

Structure your answer as:

1. What the code does
2. Step-by-step explanation
3. Important concepts used
4. Example walkthrough
5. Time complexity
6. Space complexity
"""


    elif task == "Debug Code":

        task_instruction = """
Analyze the code for bugs.

Structure your answer as:

1. Problem identified
2. Why the problem occurs
3. Exact location of the problem
4. Corrected code
5. Explanation of the fix
6. Edge cases
7. Time and space complexity
"""


    elif task == "Optimize Code":

        task_instruction = """
Analyze the code and suggest improvements.

Structure your answer as:

1. Current approach
2. Problems with the current approach
3. Optimized approach
4. Optimized code
5. Why the optimized approach is better
6. Time complexity before optimization
7. Time complexity after optimization
8. Space complexity
"""


    elif task == "Complexity Analysis":

        task_instruction = """
Analyze the algorithmic complexity.

Structure your answer as:

1. What the algorithm does
2. Time complexity
3. Detailed reason for the time complexity
4. Space complexity
5. Bottleneck
6. Possible optimization
"""


    elif task == "Code Review":

        task_instruction = """
Perform a code review.

Check:

- Correctness
- Readability
- Naming
- Structure
- Efficiency
- Error handling
- Edge cases
- Maintainability
- Potential bugs

Give an overall rating from 1 to 10.
"""


    elif task == "Convert Code":

        task_instruction = """
Convert the given code into the requested target language
if a target language is mentioned.

If no target language is provided, explain that a target
language is required.

Explain important differences between the original and
converted code.
"""


    else:

        task_instruction = """
Analyze the code and provide a useful explanation.
"""


    # ========================================================
    # Error Information
    # ========================================================

    error_section = ""

    if error_message.strip():

        error_section = f"""
USER-PROVIDED ERROR MESSAGE:

{error_message}

Use this error message during your debugging analysis.
"""


    # ========================================================
    # Final Prompt
    # ========================================================

    prompt = f"""
{base_instruction}

TASK:
{task_instruction}

PROGRAMMING LANGUAGE:
{language}

RELEVANT PROGRAMMING KNOWLEDGE:

{context}

{error_section}

USER CODE:

```{language.lower()}
{code}
