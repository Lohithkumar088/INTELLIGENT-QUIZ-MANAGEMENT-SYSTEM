from django.conf import settings
from openai import OpenAI


def call_ai_explanation_api(question_text, correct_answer, user_answer):
    """
    Generate AI explanation using OpenAI API
    (Drop-in replacement for Gemini version)
    """
    try:
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            return f"The correct answer is: {correct_answer}"

        client = OpenAI(api_key=api_key)

        prompt = f"""
Question: {question_text}
User's Answer: {user_answer}
Correct Answer: {correct_answer}

Explain clearly (in 3–4 sentences):
- Why the correct answer is correct
- What was wrong with the user's answer
Use simple, student-friendly language.
"""

        print("📚 Generating explanation using OpenAI...")

        response = client.chat.completions.create(
            model="gpt-4o-mini",   # ✅ Best balance (fast + cheap)
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful quiz assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.6,
            max_tokens=350,
        )

        if response and response.choices:
            explanation = response.choices[0].message.content.strip()
            print("✅ Explanation generated with OpenAI")
            return explanation

        print("⚠️ Empty response from OpenAI")
        return f"The correct answer is: {correct_answer}"

    except ImportError:
        print("⚠️ openai library not installed")
        return f"The correct answer is: {correct_answer}"

    except Exception as e:
        print(f"❌ OpenAI error: {type(e).__name__} – {str(e)[:100]}")
        return f"The correct answer is: {correct_answer}"