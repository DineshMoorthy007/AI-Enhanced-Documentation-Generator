import os
from openai import OpenAI

# Create client (expects OPENAI_API_KEY in env)
client = OpenAI()


def generate_file_documentation(
    file_path: str,
    functions: list,
    classes: list,
    code_snippet: str,
) -> str:
    """
    Generate documentation for a single file using an LLM.
    """

    prompt = f"""
You are a senior software engineer and technical writer.

File path:
{file_path}

Functions:
{functions}

Classes:
{classes}

Code snippet:
{code_snippet}

Task:
Explain the purpose of this file in the context of the project.
Use clear, professional technical language.
If functions or classes exist:
- Explain what problem they solve
- Explain how they are used
Avoid repeating code.
Do not speculate beyond the given code.
Write 3–5 concise sentences.

"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You generate high-quality technical documentation."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()
