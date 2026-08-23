import os
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Intelligent_Quiz.settings')
django.setup()

from quizzes.models import Category, Subcategory, AIQuestion

# Clear previous questions
AIQuestion.objects.all().delete()
print("Cleared old AIQuestion table for difficulty-based seeding.")

def gen_math_by_difficulty(diff, count):
    qs = []
    for i in range(1, count + 1):
        if diff == 'Easy':
            a = random.randint(5, 50)
            b = random.randint(5, 50)
            op = random.choice(['+', '-', '*'])
            if op == '+':
                ans_val = a + b
                q_text = f"[Easy Math Q{i}] What is the value of {a} + {b}?"
            elif op == '-':
                if a < b: a, b = b, a
                ans_val = a - b
                q_text = f"[Easy Math Q{i}] What is the value of {a} - {b}?"
            else:
                a, b = random.randint(2, 12), random.randint(2, 12)
                ans_val = a * b
                q_text = f"[Easy Math Q{i}] What is {a} multiplied by {b}?"
            
            ans = str(ans_val)
            opts = [ans, str(ans_val + 2), str(ans_val - 3 if ans_val >= 3 else ans_val + 4), str(ans_val + 5)]
        
        elif diff == 'Medium':
            topic = i % 4
            if topic == 0:
                # Quadratic roots
                r1, r2 = random.randint(1, 6), random.randint(1, 6)
                b_val = -(r1 + r2)
                c_val = r1 * r2
                q_text = f"[Medium Math Q{i}] What is one of the real roots of the quadratic equation x² + ({b_val})x + {c_val} = 0?"
                ans = str(r1)
                opts = [ans, str(r1 + 7), str(r1 + 9), str(r1 - 4)]
            elif topic == 1:
                # Exponents / Logs
                base = random.choice([2, 3, 10])
                exp = random.randint(2, 5)
                val = base ** exp
                q_text = f"[Medium Math Q{i}] What is log base {base} of {val}?"
                ans = str(exp)
                opts = [ans, str(exp + 1), str(exp - 1 if exp > 1 else 6), str(exp * 2)]
            elif topic == 2:
                # Trigonometry
                angle, sin_val = random.choice([(30, "0.5"), (90, "1.0"), (0, "0.0"), (45, "√2/2")])
                q_text = f"[Medium Math Q{i}] What is the value of sin({angle}°)?"
                ans = sin_val
                opts = [ans, "0.866", "1.5", "2.0"]
            else:
                # Probability
                q_text = f"[Medium Math Q{i}] What is the probability of rolling a prime number (2, 3, or 5) on a single 6-sided die?"
                ans = "3/6 (50%)"
                opts = [ans, "1/6 (16.6%)", "2/6 (33.3%)", "4/6 (66.6%)"]

        else: # Hard
            topic = i % 4
            if topic == 0:
                # Calculus derivative
                n = random.randint(2, 5)
                c = random.randint(2, 6)
                q_text = f"[Hard Math Q{i}] What is the derivative of f(x) = {c}x^{n} with respect to x?"
                ans = f"{c*n}x^{n-1}" if n-1 > 1 else (f"{c*n}x" if n-1 == 1 else f"{c*n}")
                opts = [ans, f"{c}x^{n-1}", f"{c*n}x^{n}", f"{c+n}x^{n-1}"]
            elif topic == 1:
                # Calculus integral
                n = random.randint(2, 4)
                q_text = f"[Hard Math Q{i}] What is the indefinite integral ∫ x^{n} dx?"
                ans = f"(x^{n+1})/({n+1}) + C"
                opts = [ans, f"(x^{n})/({n}) + C", f"{n}x^{n-1} + C", f"(x^{n+2})/({n+2}) + C"]
            elif topic == 2:
                # Matrix Determinant
                a, b, c, d = random.randint(1, 5), random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)
                det = (a * d) - (b * c)
                q_text = f"[Hard Math Q{i}] What is the determinant of the 2x2 matrix [[{a}, {b}], [{c}, {d}]]?"
                ans = str(det)
                opts = [ans, str(det + 3), str(det - 5), str(det + 8)]
            else:
                # Complex numbers
                q_text = f"[Hard Math Q{i}] What is the value of i^4 (where i is the imaginary unit √-1)?"
                ans = "1"
                opts = [ans, "i", "-1", "-i"]

        random.shuffle(opts)
        qs.append(('Academic', 'Mathematics', diff, q_text, opts, ans))
    return qs


def gen_subcat_by_difficulty(cat_name, subcat_name, diff, count):
    qs = []
    
    # Specific pre-crafted question pools per difficulty
    curated_pool = {
        ('Computer Science', 'Easy'): [
            ("What does CPU stand for?", ["Central Processing Unit", "Central Power Unit", "Computer Processing Utility", "Control Program Unit"], "Central Processing Unit"),
            ("Which device is used for long-term data storage?", ["Hard Disk / SSD", "RAM", "Cache", "CPU Registers"], "Hard Disk / SSD"),
            ("What is the primary language used to structure web pages?", ["HTML", "C++", "Python", "SQL"], "HTML"),
            ("What does RAM stand for?", ["Random Access Memory", "Read Access Method", "Rapid Application Module", "Run Active Memory"], "Random Access Memory"),
            ("Which input device is primarily used to type text?", ["Keyboard", "Monitor", "Speaker", "Printer"], "Keyboard"),
        ],
        ('Computer Science', 'Medium'): [
            ("Which data structure operates on a First In, First Out (FIFO) order?", ["Queue", "Stack", "Binary Tree", "Graph"], "Queue"),
            ("Which sorting algorithm has an average time complexity of O(n log n)?", ["Merge Sort", "Bubble Sort", "Selection Sort", "Insertion Sort"], "Merge Sort"),
            ("What type of SQL query is used to fetch records from a database table?", ["SELECT", "INSERT", "UPDATE", "DELETE"], "SELECT"),
            ("What is an Object-Oriented Programming (OOP) pillar that hides internal implementation details?", ["Encapsulation", "Inheritance", "Polymorphism", "Recursion"], "Encapsulation"),
            ("Which HTTP status code indicates a successful request?", ["200 OK", "404 Not Found", "500 Internal Server Error", "301 Moved Permanently"], "200 OK"),
        ],
        ('Computer Science', 'Hard'): [
            ("What is a condition where two or more threads are blocked forever waiting for each other?", ["Deadlock", "Race Condition", "Starvation", "Page Fault"], "Deadlock"),
            ("What is the worst-case time complexity of Quick Sort?", ["O(n²)", "O(n log n)", "O(n)", "O(log n)"], "O(n²)"),
            ("Which page replacement algorithm suffers from Belady's Anomaly?", ["FIFO (First In First Out)", "LRU (Least Recently Used)", "Optimal", "LFU"], "FIFO (First In First Out)"),
            ("What is the primary function of a Translation Lookaside Buffer (TLB)?", ["Cache virtual-to-physical address translations", "Store CPU instruction cache", "Manage disk I/O buffers", "Handle network packets"], "Cache virtual-to-physical address translations"),
            ("In B-Trees of order m, what is the maximum number of children a node can have?", ["m", "m-1", "2m", "m/2"], "m"),
        ],
        ('Artificial Intelligence', 'Easy'): [
            ("What is the primary goal of Artificial Intelligence?", ["Enable machines to simulate human intelligence", "Build faster hardware fans", "Create website layouts", "Store raw database records"], "Enable machines to simulate human intelligence"),
            ("What does AI stand for?", ["Artificial Intelligence", "Automated Information", "Applied Integration", "Advanced Algorithm"], "Artificial Intelligence"),
            ("Which field of AI deals with speech and written human language?", ["Natural Language Processing (NLP)", "Computer Vision", "Robotics", "Quantum Computing"], "Natural Language Processing (NLP)"),
        ],
        ('Artificial Intelligence', 'Medium'): [
            ("Which machine learning task involves finding clusters in unlabelled data?", ["Unsupervised Learning", "Supervised Learning", "Reinforcement Learning", "Classification"], "Unsupervised Learning"),
            ("What neural network architecture is tailored for spatial image analysis?", ["Convolutional Neural Network (CNN)", "Recurrent Neural Network (RNN)", "Multi-layer Perceptron", "Hopfield Network"], "Convolutional Neural Network (CNN)"),
            ("What evaluation metric measures the proportion of actual positives correctly identified?", ["Recall / Sensitivity", "Precision", "Accuracy", "Specificity"], "Recall / Sensitivity"),
        ],
        ('Artificial Intelligence', 'Hard'): [
            ("What mechanism allows Transformer architectures to model long-range dependencies efficiently?", ["Scaled Dot-Product Self-Attention", "Recurrent Backpropagation Through Time", "Max Pooling", "Gradient Clipping"], "Scaled Dot-Product Self-Attention"),
            ("What problem occurs when gradients shrink exponentially during deep network backpropagation?", ["Vanishing Gradient Problem", "Exploding Gradient Problem", "Overfitting", "Mode Collapse"], "Vanishing Gradient Problem"),
            ("What loss function is standard for training Generative Adversarial Networks (GANs)?", ["Minimax Adversarial Loss", "Mean Squared Error", "Cross-Entropy Loss", "Hinge Loss"], "Minimax Adversarial Loss"),
        ],
        ('Python Programming', 'Easy'): [
            ("Which keyword is used to define a function in Python?", ["def", "function", "fn", "define"], "def"),
            ("How do you write a single-line comment in Python?", ["#", "//", "/*", "--"], "#"),
            ("Which operator is used for exponentiation (power) in Python?", ["**", "^", "pow", "exp"], "**"),
        ],
        ('Python Programming', 'Medium'): [
            ("What does the 'yield' keyword do in a Python function?", ["Turns the function into a generator", "Exits the function permanently", "Raises an exception", "Imports a module"], "Turns the function into a generator"),
            ("Which method removes and returns the last item from a list?", ["pop()", "remove()", "delete()", "extract()"], "pop()"),
            ("What is the purpose of the built-in zip() function?", ["Iterates over multiple iterables in parallel", "Compresses files into zip format", "Sorts two lists", "Encodes strings"], "Iterates over multiple iterables in parallel"),
        ],
        ('Python Programming', 'Hard'): [
            ("What is the Global Interpreter Lock (GIL) in CPython?", ["A mutex that prevents multiple native threads from executing Python bytecode simultaneously", "A security sandbox for executing untrusted code", "A garbage collector lock", "A compiler optimization phase"], "A mutex that prevents multiple native threads from executing Python bytecode simultaneously"),
            ("What decorator is used to define a class method that receives the class as its first parameter?", ["@classmethod", "@staticmethod", "@property", "@abstractmethod"], "@classmethod"),
            ("Which dunder method is called when an attribute lookup fails in an object?", ["__getattr__", "__getattribute__", "__getitem__", "__findattr__"], "__getattr__"),
        ],
    }

    pool = curated_pool.get((subcat_name, diff), [])

    for i in range(1, count + 1):
        if i - 1 < len(pool):
            q_text, opts, ans = pool[i - 1]
            opts = list(opts)
        else:
            q_text = f"[{subcat_name} - {diff}] Question #{i}: What is a key concept specific to {diff} level {subcat_name}?"
            ans = f"{diff} Concept #{i} of {subcat_name}"
            opts = [
                ans,
                f"{diff} Distractor A for {subcat_name}",
                f"{diff} Distractor B in {cat_name}",
                f"Basic misconception C"
            ]
        
        random.shuffle(opts)
        qs.append((cat_name, subcat_name, diff, q_text, opts, ans))

    return qs


def main():
    categories = Category.objects.all().prefetch_related('subcategories')
    bulk_objects = []

    for category in categories:
        for subcat in category.subcategories.all():
            # 34 Easy, 33 Medium, 33 Hard = 100 questions per subcategory
            for diff, count in [('Easy', 34), ('Medium', 33), ('Hard', 33)]:
                if subcat.name == 'Mathematics':
                    items = gen_math_by_difficulty(diff, count)
                else:
                    items = gen_subcat_by_difficulty(category.name, subcat.name, diff, count)

                for cat_n, subcat_n, difficulty, q_text, opts, ans in items:
                    bulk_objects.append(AIQuestion(
                        category=cat_n,
                        subcategory=subcat_n,
                        difficulty=difficulty,
                        question_text=q_text,
                        options=opts,
                        answer=ans
                    ))

    AIQuestion.objects.bulk_create(bulk_objects)
    print(f"🎉 Successfully created {len(bulk_objects)} difficulty-categorized questions in DB!")

    # Verify counts per difficulty
    for diff in ['Easy', 'Medium', 'Hard']:
        c = AIQuestion.objects.filter(difficulty=diff).count()
        print(f"  - {diff} questions total: {c}")

if __name__ == '__main__':
    main()
