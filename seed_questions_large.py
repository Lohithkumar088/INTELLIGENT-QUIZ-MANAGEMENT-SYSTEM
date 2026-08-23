import os
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Intelligent_Quiz.settings')
django.setup()

from quizzes.models import Category, Subcategory, AIQuestion

# Clear previous AIQuestions to avoid duplicates
AIQuestion.objects.all().delete()
print("Cleared old AIQuestion database records.")

# Helper math generators
def gen_math_questions(count=100):
    qs = []
    difficulties = ['Easy'] * 34 + ['Medium'] * 33 + ['Hard'] * 33
    for i in range(count):
        diff = difficulties[i]
        if diff == 'Easy':
            a, b = random.randint(2, 20), random.randint(2, 20)
            op = random.choice(['+', '-', '*'])
            if op == '+': ans_val = a + b
            elif op == '-': ans_val = a - b
            else: ans_val = a * b
            q_text = f"What is the result of {a} {op} {b}?"
            ans = str(ans_val)
            opts = [ans, str(ans_val + 2), str(ans_val - 3), str(ans_val + 5)]
        elif diff == 'Medium':
            a, b = random.randint(10, 50), random.randint(2, 12)
            q_text = f"Solve for x in the equation: {b}x - {a} = {b*random.randint(2,10) - a}"
            x_val = (int(q_text.split('=')[1].strip()) + a) // b
            ans = str(x_val)
            opts = [ans, str(x_val + 1), str(x_val - 2), str(x_val + 3)]
        else:
            n = random.randint(5, 15)
            q_text = f"What is the sum of the first {n} positive integers?"
            ans_val = (n * (n + 1)) // 2
            ans = str(ans_val)
            opts = [ans, str(ans_val + n), str(ans_val - 5), str(ans_val + 10)]
        
        random.shuffle(opts)
        qs.append(('Academic', 'Mathematics', diff, q_text, opts, ans))
    return qs

def gen_questions_for_subcat(cat_name, subcat_name):
    # Specialized dataset or structured topic generator
    qs = []
    difficulties = ['Easy'] * 34 + ['Medium'] * 33 + ['Hard'] * 33
    
    # Pre-crafted topic banks
    topic_banks = {
        'History': [
            ("In which year did World War II end?", ["1945", "1939", "1918", "1950"], "1945"),
            ("Who was the first President of the United States?", ["George Washington", "Thomas Jefferson", "Abraham Lincoln", "John Adams"], "George Washington"),
            ("Which ancient empire constructed the Colosseum in Rome?", ["Roman Empire", "Ottoman Empire", "Byzantine Empire", "Greek Empire"], "Roman Empire"),
            ("In which year did the French Revolution begin?", ["1789", "1776", "1804", "1815"], "1789"),
            ("Who wrote the Declaration of Independence?", ["Thomas Jefferson", "Benjamin Franklin", "Alexander Hamilton", "George Washington"], "Thomas Jefferson"),
            ("Which ancient civilization built the Pyramids of Giza?", ["Ancient Egyptians", "Mayans", "Babylonians", "Persians"], "Ancient Egyptians"),
            ("Which Treaty officially ended World War I in 1919?", ["Treaty of Versailles", "Treaty of Paris", "Treaty of Ghent", "Treaty of Utrecht"], "Treaty of Versailles"),
            ("Who was the British Prime Minister during most of World War II?", ["Winston Churchill", "Neville Chamberlain", "Clement Attlee", "Harold Macmillan"], "Winston Churchill"),
            ("The Fall of the Berlin Wall occurred in which year?", ["1989", "1991", "1987", "1979"], "1989"),
            ("Which ancient empire built Machu Picchu?", ["Inca Empire", "Aztec Empire", "Maya Empire", "Olmec Empire"], "Inca Empire"),
        ],
        'Geography': [
            ("What is the largest ocean on Earth?", ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"], "Pacific Ocean"),
            ("Which country has the largest land area in the world?", ["Russia", "Canada", "China", "United States"], "Russia"),
            ("What is the longest river in the world?", ["Nile River", "Amazon River", "Yangtze River", "Mississippi River"], "Nile River"),
            ("Mount Everest is located in which mountain range?", ["Himalayas", "Andes", "Alps", "Rocky Mountains"], "Himalayas"),
            ("What is the capital city of Japan?", ["Tokyo", "Kyoto", "Osaka", "Hiroshima"], "Tokyo"),
            ("Which continent is home to the Amazon Rainforest?", ["South America", "Africa", "Asia", "North America"], "South America"),
            ("What is the smallest country in the world by area?", ["Vatican City", "Monaco", "San Marino", "Liechtenstein"], "Vatican City"),
            ("Which country contains the Great Barrier Reef?", ["Australia", "Indonesia", "Philippines", "Fiji"], "Australia"),
        ],
        'Computer Science': [
            ("What does CPU stand for?", ["Central Processing Unit", "Central Power Unit", "Computer Processing Utility", "Control Program Unit"], "Central Processing Unit"),
            ("Which data structure operates on a First In, First Out (FIFO) basis?", ["Queue", "Stack", "Tree", "Graph"], "Queue"),
            ("What is the primary function of an Operating System?", ["Manage system resources and hardware", "Design web pages", "Compile Python code", "Perform database queries"], "Manage system resources and hardware"),
            ("Which sorting algorithm has a worst-case time complexity of O(n^2)?", ["Bubble Sort", "Merge Sort", "Quick Sort", "Heap Sort"], "Bubble Sort"),
            ("What is the main purpose of an IP address?", ["Identify devices on a network", "Store local files", "Encrypt password hashes", "Speed up CPU clock"], "Identify devices on a network"),
        ],
        'Artificial Intelligence': [
            ("What is the primary objective of Machine Learning?", ["Learn patterns from data to make predictions", "Write static IF statements", "Build faster processors", "Create database schemas"], "Learn patterns from data to make predictions"),
            ("Which neural network architecture is widely used for computer vision?", ["Convolutional Neural Network (CNN)", "Recurrent Neural Network (RNN)", "Perceptron", "Transformer"], "Convolutional Neural Network (CNN)"),
            ("What is Supervised Learning?", ["Training with labeled input-output data", "Training without any labels", "Learning through trial and rewards", "Clustering raw data"], "Training with labeled input-output data"),
            ("What does NLP stand for in Artificial Intelligence?", ["Natural Language Processing", "Neural Language Parsing", "Network Logic Protocol", "Numerical Linear Programming"], "Natural Language Processing"),
            ("What model architecture introduced Self-Attention mechanisms?", ["Transformers", "Decision Trees", "K-Means", "Support Vector Machines"], "Transformers"),
        ],
        'Python Programming': [
            ("Which keyword is used to define a function in Python?", ["def", "function", "fn", "define"], "def"),
            ("What data type is returned by range() in Python 3?", ["range object", "list", "tuple", "set"], "range object"),
            ("How do you start a single-line comment in Python?", ["#", "//", "/*", "--"], "#"),
            ("Which built-in method adds an item to the end of a list?", ["append()", "add()", "insert()", "push()"], "append()"),
            ("What is the output of print(type([])) in Python?", ["<class 'list'>", "<class 'array'>", "<class 'tuple'>", "<class 'dict'>"], "<class 'list'>"),
        ],
        'Web Development': [
            ("What does HTML stand for?", ["HyperText Markup Language", "HighText Transfer Machine Language", "Hyperlink Text Manipulation Language", "Home Tool Markup Language"], "HyperText Markup Language"),
            ("Which CSS property is used to change text color?", ["color", "font-color", "text-style", "background-color"], "color"),
            ("Which JS keyword declares a block-scoped constant variable?", ["const", "let", "var", "static"], "const"),
            ("What does HTTP status code 404 signify?", ["Not Found", "OK / Success", "Server Error", "Unauthorized"], "Not Found"),
            ("Which HTML tag embeds an image?", ["<img>", "<image>", "<picture>", "<src>"], "<img>"),
        ]
    }

    base_samples = topic_banks.get(subcat_name, [])

    for i in range(100):
        diff = difficulties[i]
        if i < len(base_samples):
            q_text, opts, ans = base_samples[i]
            opts = list(opts)
        else:
            num = i + 1
            q_text = f"[{subcat_name} - {diff}] Question #{num}: Which statement accurately describes a key principle of {subcat_name}?"
            ans = f"Primary principle #{num} of {subcat_name}"
            opts = [
                ans,
                f"Secondary property A of {subcat_name}",
                f"Alternative formulation B in {cat_name}",
                f"Common misconception C"
            ]
        
        random.shuffle(opts)
        qs.append((cat_name, subcat_name, diff, q_text, opts, ans))

    return qs

def main():
    total_created = 0
    categories = Category.objects.all().prefetch_related('subcategories')
    
    all_objects = []
    
    for category in categories:
        for subcat in category.subcategories.all():
            if subcat.name == 'Mathematics':
                items = gen_math_questions(100)
            else:
                items = gen_questions_for_subcat(category.name, subcat.name)
            
            for cat_n, subcat_n, diff, q_text, opts, ans in items:
                all_objects.append(AIQuestion(
                    category=cat_n,
                    subcategory=subcat_n,
                    difficulty=diff,
                    question_text=q_text,
                    options=opts,
                    answer=ans
                ))

    # Bulk create for fast insertion of 4100 questions
    AIQuestion.objects.bulk_create(all_objects)
    print(f"🎉 Successfully created {len(all_objects)} questions in the database!")
    print(f"Total AIQuestion records in DB: {AIQuestion.objects.count()}")

if __name__ == '__main__':
    main()
