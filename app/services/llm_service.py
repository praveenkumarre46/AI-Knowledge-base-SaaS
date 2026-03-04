import ollama


def generate_answer(question, contexts):

    context_text = "\n".join(contexts)

    prompt = f"""
You are an AI assistant answering questions using the provided context.

Context:
{context_text}

Question:
{question}

Answer clearly based only on the context.
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]