import json
import time
from django.conf import settings
from openai import OpenAI
from quizzes.models import AIQuestion


def generate_questions(
    category,
    subcategory,
    difficulty,
    num_questions,
    max_retries=2,
):
    """
    Generate quiz questions using OpenAI API.

    Features:
    - Retry logic
    - Strict JSON-only output
    - Validation
    - Database fallback
    """

def get_offline_fallback_questions(category, subcategory, difficulty, count, start_idx=1):
    """
    Generate distinct, subject-specific fallback quiz questions offline.
    """
    questions = []
    sample_topics = {
        'Mathematics': [
            ("What is the value of Pi rounded to two decimal places?", ["3.14", "3.16", "3.12", "3.18"], "3.14"),
            ("What is the square root of 144?", ["12", "14", "10", "16"], "12"),
            ("What is the sum of interior angles in a triangle?", ["180 degrees", "360 degrees", "90 degrees", "270 degrees"], "180 degrees"),
            ("Solve for x: 3x - 5 = 10", ["5", "3", "4", "6"], "5"),
            ("What is 7 multiplied by 8?", ["56", "54", "48", "64"], "56"),
            ("What is the Pythagorean theorem formula for a right triangle?", ["a^2 + b^2 = c^2", "a + b = c", "a * b = c", "a^2 - b^2 = c^2"], "a^2 + b^2 = c^2"),
            ("What is the median of [2, 5, 7, 10, 12]?", ["7", "5", "8", "6"], "7"),
            ("What is 2 raised to the power of 5?", ["32", "16", "64", "25"], "32"),
            ("What is the area formula for a circle with radius r?", ["πr²", "2πr", "πr", "4πr²"], "πr²"),
            ("What is 15% of 200?", ["30", "25", "35", "20"], "30"),
        ],
        'History': [
            ("In which year did World War II end?", ["1945", "1939", "1918", "1950"], "1945"),
            ("Who was the first President of the United States?", ["George Washington", "Thomas Jefferson", "Abraham Lincoln", "John Adams"], "George Washington"),
            ("Which ancient empire constructed the Colosseum in Rome?", ["Roman Empire", "Ottoman Empire", "Byzantine Empire", "Greek Empire"], "Roman Empire"),
            ("In which year did the French Revolution begin?", ["1789", "1776", "1804", "1815"], "1789"),
            ("Who wrote the Declaration of Independence?", ["Thomas Jefferson", "Benjamin Franklin", "Alexander Hamilton", "George Washington"], "Thomas Jefferson"),
            ("Which ancient civilization built the Pyramids of Giza?", ["Ancient Egyptians", "Mayans", "Babylonians", "Persians"], "Ancient Egyptians"),
            ("Which Treaty officially ended World War I in 1919?", ["Treaty of Versailles", "Treaty of Paris", "Treaty of Ghent", "Treaty of Utrecht"], "Treaty of Versailles"),
            ("Who was the British Prime Minister during most of World War II?", ["Winston Churchill", "Neville Chamberlain", "Clement Attlee", "Harold Macmillan"], "Winston Churchill"),
        ],
        'Computer Science': [
            ("What is the primary function of an Operating System?", ["Manage system resources and hardware", "Design web pages", "Compile Python code", "Perform database queries"], "Manage system resources and hardware"),
            ("Which data structure operates on a First In, First Out (FIFO) basis?", ["Queue", "Stack", "Tree", "Graph"], "Queue"),
            ("What does CPU stand for?", ["Central Processing Unit", "Central Power Unit", "Computer Processing Utility", "Control Program Unit"], "Central Processing Unit"),
            ("Which sorting algorithm has a worst-case time complexity of O(n^2)?", ["Bubble Sort", "Merge Sort", "Quick Sort", "Heap Sort"], "Bubble Sort"),
            ("What is the main purpose of an IP address?", ["Identify devices on a network", "Store local files", "Encrypt password hashes", "Speed up CPU clock"], "Identify devices on a network"),
        ],
        'Artificial Intelligence': [
            ("What is the main goal of Machine Learning?", ["Learn patterns from data to make predictions", "Manually code IF-ELSE logic", "Build faster computer hardware", "Create database tables"], "Learn patterns from data to make predictions"),
            ("Which neural network architecture is widely used for computer vision tasks?", ["Convolutional Neural Network (CNN)", "Recurrent Neural Network (RNN)", "Multilayer Perceptron (MLP)", "Transformer"], "Convolutional Neural Network (CNN)"),
            ("What is Supervised Learning?", ["Training with labeled input-output pairs", "Training without target labels", "Learning via trial and error rewards", "Clustering raw data"], "Training with labeled input-output pairs"),
            ("Which evaluation metric measures the ratio of true positives to all positive predictions?", ["Precision", "Recall", "Accuracy", "F1 Score"], "Precision"),
            ("What does NLP stand for in AI?", ["Natural Language Processing", "Neural Language Parsing", "Network Logic Protocol", "Numerical Linear Programming"], "Natural Language Processing"),
        ],
        'Python Programming': [
            ("Which keyword is used to define a function in Python?", ["def", "function", "fn", "define"], "def"),
            ("What data type is returned by the range() function in Python 3?", ["range object", "list", "tuple", "set"], "range object"),
            ("How do you start a single-line comment in Python?", ["#", "//", "/*", "--"], "#"),
            ("Which built-in method adds an element to the end of a list?", ["append()", "add()", "insert()", "push()"], "append()"),
            ("What is the output of print(type([])) in Python?", ["<class 'list'>", "<class 'array'>", "<class 'tuple'>", "<class 'dict'>"], "<class 'list'>"),
        ],
    }

    subcat_samples = sample_topics.get(subcategory, [])

    for i in range(count):
        idx = (start_idx - 1 + i)
        if idx < len(subcat_samples):
            q_text, opts, ans = subcat_samples[idx]
        else:
            q_num = idx + 1
            q_text = f"Which of the following is an essential concept in {subcategory}?"
            ans = f"Standard principle of {subcategory}"
            opts = [
                ans,
                f"Secondary component in {category}",
                f"Alternative formulation in {subcategory}",
                f"Related concept in {category}"
            ]
            import random
            random.shuffle(opts)

        questions.append({
            "question": q_text,
            "options": opts,
            "answer": ans,
        })

    return questions


def generate_questions(
    category,
    subcategory,
    difficulty,
    num_questions,
    max_retries=2,
):
    """
    Generate quiz questions using OpenAI API with automatic fallback to DB and offline generator.
    """

    api_key = getattr(settings, "OPENAI_API_KEY", None)

    if api_key:
        client = OpenAI(api_key=api_key)

        prompt = f"""
Generate {num_questions} high-quality multiple-choice quiz questions.

Category: {category}
Subcategory: {subcategory}
Difficulty: {difficulty}

Rules:
- Each question must have exactly 4 options
- Only ONE correct answer
- Answer must exactly match one option
- Return ONLY valid JSON
- No markdown, no explanation text

JSON format:
[
  {{
    "question": "Question text",
    "options": ["A", "B", "C", "D"],
    "answer": "Correct option text"
  }}
]
"""

        # -------------- AI Attempts --------------
        for attempt in range(1, max_retries + 1):
            try:
                print(f"\n🤖 OpenAI Attempt {attempt}/{max_retries}")

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a quiz question generator."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=1400,
                )

                content = response.choices[0].message.content.strip()

                if content.startswith("```"):
                    content = content.replace("```json", "").replace("```", "").strip()

                questions = json.loads(content)

                validated = []
                for idx, q in enumerate(questions, 1):
                    if not all(k in q for k in ("question", "options", "answer")):
                        continue

                    if not isinstance(q["options"], list) or len(q["options"]) != 4:
                        continue

                    if q["answer"] not in q["options"]:
                        continue

                    validated.append(q)

                if validated:
                    print(f"✅ OpenAI success — {len(validated)} questions generated")
                    return validated

            except Exception as e:
                print(f"❌ OpenAI error: {type(e).__name__} – {str(e)[:120]}")
                time.sleep(1)
    else:
        print("⚠️ OPENAI_API_KEY not configured — using database/offline fallback")

    # -------------- Database & Offline Fallback --------------
    try:
        existing = list(AIQuestion.objects.filter(
            category=category,
            subcategory=subcategory,
            difficulty=difficulty,
        ).order_by("-created_at")[:num_questions])

        results = [
            {
                "question": q.question_text,
                "options": q.options,
                "answer": q.answer,
            }
            for q in existing
        ]

        if len(results) >= num_questions:
            print(f"✅ Loaded {len(results)} questions from DB")
            return results[:num_questions]

        needed = num_questions - len(results)
        print(f"ℹ️ Generating {needed} fallback questions for {subcategory} ({difficulty})")
        fallback_qs = get_offline_fallback_questions(category, subcategory, difficulty, needed, start_idx=len(results)+1)
        results.extend(fallback_qs)

        return results

    except Exception as e:
        print(f"❌ DB fallback error: {e}")
        return get_offline_fallback_questions(category, subcategory, difficulty, num_questions)


# ------------------------------------------------------------------
# OPTIONAL UTILITY (kept for safety / future use)
# ------------------------------------------------------------------

def parse_ai_response_safely(response_text):
    """
    Safely parse AI response that might contain markdown formatting.
    """
    try:
        if response_text.startswith("```"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()

        return json.loads(response_text)

    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        return []