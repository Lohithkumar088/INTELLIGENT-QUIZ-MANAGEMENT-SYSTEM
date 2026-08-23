import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Intelligent_Quiz.settings')
django.setup()

from quizzes.models import AIQuestion

QUESTION_BANK = [
    # Academic -> Mathematics
    ('Academic', 'Mathematics', 'Easy', 'What is the value of Pi rounded to two decimal places?', ['3.14', '3.16', '3.12', '3.18'], '3.14'),
    ('Academic', 'Mathematics', 'Easy', 'What is the square root of 144?', ['12', '14', '10', '16'], '12'),
    ('Academic', 'Mathematics', 'Easy', 'What is the sum of interior angles in a triangle?', ['180 degrees', '360 degrees', '90 degrees', '270 degrees'], '180 degrees'),
    ('Academic', 'Mathematics', 'Easy', 'Solve for x: 3x - 5 = 10', ['5', '3', '4', '6'], '5'),
    ('Academic', 'Mathematics', 'Easy', 'What is 7 multiplied by 8?', ['56', '54', '48', '64'], '56'),
    ('Academic', 'Mathematics', 'Easy', 'What is the Pythagorean theorem formula for a right triangle?', ['a^2 + b^2 = c^2', 'a + b = c', 'a * b = c', 'a^2 - b^2 = c^2'], 'a^2 + b^2 = c^2'),
    ('Academic', 'Mathematics', 'Easy', 'What is the median of [2, 5, 7, 10, 12]?', ['7', '5', '8', '6'], '7'),
    ('Academic', 'Mathematics', 'Easy', 'What is 2 raised to the power of 5?', ['32', '16', '64', '25'], '32'),
    ('Academic', 'Mathematics', 'Easy', 'What is the area formula for a circle with radius r?', ['πr²', '2πr', 'πr', '4πr²'], 'πr²'),
    ('Academic', 'Mathematics', 'Easy', 'What is 15% of 200?', ['30', '25', '35', '20'], '30'),

    # Academic -> History
    ('Academic', 'History', 'Easy', 'In which year did World War II end?', ['1945', '1939', '1918', '1950'], '1945'),
    ('Academic', 'History', 'Easy', 'Who was the first President of the United States?', ['George Washington', 'Thomas Jefferson', 'Abraham Lincoln', 'John Adams'], 'George Washington'),
    ('Academic', 'History', 'Easy', 'Which ancient empire constructed the Colosseum in Rome?', ['Roman Empire', 'Ottoman Empire', 'Byzantine Empire', 'Greek Empire'], 'Roman Empire'),
    ('Academic', 'History', 'Easy', 'In which year did the French Revolution begin?', ['1789', '1776', '1804', '1815'], '1789'),
    ('Academic', 'History', 'Easy', 'Who wrote the Declaration of Independence?', ['Thomas Jefferson', 'Benjamin Franklin', 'Alexander Hamilton', 'George Washington'], 'Thomas Jefferson'),
    ('Academic', 'History', 'Easy', 'Which ancient civilization built the Pyramids of Giza?', ['Ancient Egyptians', 'Mayans', 'Babylonians', 'Persians'], 'Ancient Egyptians'),
    ('Academic', 'History', 'Easy', 'Who was the first emperor of China who united the country in 221 BC?', ['Qin Shi Huang', 'Han Wudi', 'Kublai Khan', 'Sun Tzu'], 'Qin Shi Huang'),
    ('Academic', 'History', 'Easy', 'Which war took place between 1914 and 1918?', ['World War I', 'World War II', 'Thirty Years War', 'Napoleonic War'], 'World War I'),
    ('Academic', 'History', 'Easy', 'Who was the famous queen of ancient Egypt who aligned with Julius Caesar?', ['Cleopatra', 'Nefertiti', 'Hatshepsut', 'Isis'], 'Cleopatra'),
    ('Academic', 'History', 'Easy', 'The Magna Carta was signed in England in which year?', ['1215', '1066', '1314', '1492'], '1215'),

    # Academic -> Geography
    ('Academic', 'Geography', 'Easy', 'What is the largest ocean on Earth?', ['Pacific Ocean', 'Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean'], 'Pacific Ocean'),
    ('Academic', 'Geography', 'Easy', 'Which country has the largest land area in the world?', ['Russia', 'Canada', 'China', 'United States'], 'Russia'),
    ('Academic', 'Geography', 'Easy', 'What is the longest river in the world?', ['Nile River', 'Amazon River', 'Yangtze River', 'Mississippi River'], 'Nile River'),
    ('Academic', 'Geography', 'Easy', 'Mount Everest is located in which mountain range?', ['Himalayas', 'Andes', 'Alps', 'Rocky Mountains'], 'Himalayas'),
    ('Academic', 'Geography', 'Easy', 'What is the capital city of Japan?', ['Tokyo', 'Kyoto', 'Osaka', 'Hiroshima'], 'Tokyo'),
    ('Academic', 'Geography', 'Easy', 'Which continent is home to the Amazon Rainforest?', ['South America', 'Africa', 'Asia', 'North America'], 'South America'),
    ('Academic', 'Geography', 'Easy', 'What is the smallest country in the world by area?', ['Vatican City', 'Monaco', 'San Marino', 'Liechtenstein'], 'Vatican City'),
    ('Academic', 'Geography', 'Easy', 'Which country contains the Great Barrier Reef?', ['Australia', 'Indonesia', 'Philippines', 'Fiji'], 'Australia'),

    # Academic -> Physics
    ('Academic', 'Physics', 'Easy', 'What is Newton\'s First Law of Motion also known as?', ['Law of Inertia', 'Law of Gravity', 'Law of Action-Reaction', 'Law of Momentum'], 'Law of Inertia'),
    ('Academic', 'Physics', 'Easy', 'What is the speed of light in a vacuum?', ['3 x 10^8 m/s', '3 x 10^6 m/s', '1.5 x 10^8 m/s', '3 x 10^10 m/s'], '3 x 10^8 m/s'),
    ('Academic', 'Physics', 'Easy', 'What unit is used to measure electrical resistance?', ['Ohm', 'Volt', 'Ampere', 'Watt'], 'Ohm'),
    ('Academic', 'Physics', 'Easy', 'Which subatomic particle carries a negative electric charge?', ['Electron', 'Proton', 'Neutron', 'Photon'], 'Electron'),
    ('Academic', 'Physics', 'Easy', 'What is the SI unit of Force?', ['Newton', 'Joule', 'Pascal', 'Watt'], 'Newton'),

    # Academic -> Chemistry
    ('Academic', 'Chemistry', 'Easy', 'What is the chemical symbol for Gold?', ['Au', 'Ag', 'Fe', 'Cu'], 'Au'),
    ('Academic', 'Chemistry', 'Easy', 'What is the pH level of pure water?', ['7', '0', '14', '5'], '7'),
    ('Academic', 'Chemistry', 'Easy', 'Which element has the atomic number 1?', ['Hydrogen', 'Helium', 'Carbon', 'Oxygen'], 'Hydrogen'),
    ('Academic', 'Chemistry', 'Easy', 'What is the chemical formula for common table salt?', ['NaCl', 'H2O', 'CO2', 'KCl'], 'NaCl'),
    ('Academic', 'Chemistry', 'Easy', 'What gas is most abundant in Earth\'s atmosphere?', ['Nitrogen', 'Oxygen', 'Argon', 'Carbon Dioxide'], 'Nitrogen'),

    # Academic -> Biology
    ('Academic', 'Biology', 'Easy', 'What is known as the powerhouse of the cell?', ['Mitochondria', 'Nucleus', 'Ribosome', 'Golgi Apparatus'], 'Mitochondria'),
    ('Academic', 'Biology', 'Easy', 'What process do plants use to make food using sunlight?', ['Photosynthesis', 'Respiration', 'Transpiration', 'Fermentation'], 'Photosynthesis'),
    ('Academic', 'Biology', 'Easy', 'How many chromosomes do human somatic cells normally contain?', ['46', '23', '48', '44'], '46'),
    ('Academic', 'Biology', 'Easy', 'Which pigment gives plants their green color?', ['Chlorophyll', 'Melanin', 'Hemoglobin', 'Carotene'], 'Chlorophyll'),
    ('Academic', 'Biology', 'Easy', 'What is the main function of Red Blood Cells?', ['Transport oxygen', 'Fight infections', 'Clot blood', 'Digest food'], 'Transport oxygen'),

    # Science & Tech -> Computer Science
    ('Science & Tech', 'Computer Science', 'Easy', 'What does CPU stand for?', ['Central Processing Unit', 'Central Power Unit', 'Computer Processing Utility', 'Control Program Unit'], 'Central Processing Unit'),
    ('Science & Tech', 'Computer Science', 'Easy', 'Which data structure operates on a First In, First Out (FIFO) basis?', ['Queue', 'Stack', 'Tree', 'Graph'], 'Queue'),
    ('Science & Tech', 'Computer Science', 'Easy', 'What is the primary function of an Operating System?', ['Manage system resources and hardware', 'Design graphics', 'Compile code', 'Execute SQL'], 'Manage system resources and hardware'),
    ('Science & Tech', 'Computer Science', 'Easy', 'Which sorting algorithm has a worst-case time complexity of O(n^2)?', ['Bubble Sort', 'Merge Sort', 'Quick Sort', 'Heap Sort'], 'Bubble Sort'),
    ('Science & Tech', 'Computer Science', 'Easy', 'What is the main purpose of an IP address?', ['Identify devices on a network', 'Encrypt passwords', 'Store files', 'Increase CPU speed'], 'Identify devices on a network'),

    # Science & Tech -> Artificial Intelligence
    ('Science & Tech', 'Artificial Intelligence', 'Easy', 'What is the primary objective of Machine Learning?', ['Learn patterns from data to make predictions', 'Write static IF statements', 'Build faster processors', 'Create database schemas'], 'Learn patterns from data to make predictions'),
    ('Science & Tech', 'Artificial Intelligence', 'Easy', 'Which neural network architecture is widely used for computer vision?', ['Convolutional Neural Network (CNN)', 'Recurrent Neural Network (RNN)', 'Perceptron', 'Transformer'], 'Convolutional Neural Network (CNN)'),
    ('Science & Tech', 'Artificial Intelligence', 'Easy', 'What is Supervised Learning?', ['Training with labeled input-output data', 'Training without any labels', 'Learning through trial and rewards', 'Clustering raw data'], 'Training with labeled input-output data'),
    ('Science & Tech', 'Artificial Intelligence', 'Easy', 'What does NLP stand for in Artificial Intelligence?', ['Natural Language Processing', 'Neural Language Parsing', 'Network Logic Protocol', 'Numerical Linear Programming'], 'Natural Language Processing'),
    ('Science & Tech', 'Artificial Intelligence', 'Easy', 'What model architecture introduced Self-Attention mechanisms?', ['Transformers', 'Decision Trees', 'K-Means', 'Support Vector Machines'], 'Transformers'),

    # Technology -> Python Programming
    ('Technology', 'Python Programming', 'Easy', 'Which keyword is used to define a function in Python?', ['def', 'function', 'fn', 'define'], 'def'),
    ('Technology', 'Python Programming', 'Easy', 'What data type is returned by range() in Python 3?', ['range object', 'list', 'tuple', 'set'], 'range object'),
    ('Technology', 'Python Programming', 'Easy', 'How do you start a single-line comment in Python?', ['#', '//', '/*', '--'], '#'),
    ('Technology', 'Python Programming', 'Easy', 'Which built-in method adds an item to the end of a list?', ['append()', 'add()', 'insert()', 'push()'], 'append()'),
    ('Technology', 'Python Programming', 'Easy', 'What is the output of type([]) in Python?', ["<class 'list'>", "<class 'array'>", "<class 'tuple'>", "<class 'dict'>"], "<class 'list'>"),

    # Technology -> Web Development
    ('Technology', 'Web Development', 'Easy', 'What does HTML stand for?', ['HyperText Markup Language', 'HighText Transfer Machine Language', 'Hyperlink Text Manipulation Language', 'Home Tool Markup Language'], 'HyperText Markup Language'),
    ('Technology', 'Web Development', 'Easy', 'Which CSS property is used to change text color?', ['color', 'font-color', 'text-style', 'background-color'], 'color'),
    ('Technology', 'Web Development', 'Easy', 'Which JS keyword declares a block-scoped constant variable?', ['const', 'let', 'var', 'static'], 'const'),
    ('Technology', 'Web Development', 'Easy', 'What does HTTP status code 404 signify?', ['Not Found', 'OK / Success', 'Server Error', 'Unauthorized'], 'Not Found'),
    ('Technology', 'Web Development', 'Easy', 'Which HTML tag embeds an image?', ['<img>', '<image>', '<picture>', '<src>'], '<img>'),
]

def seed_db():
    created_count = 0
    for cat, subcat, diff, q_text, opts, ans in QUESTION_BANK:
        obj, created = AIQuestion.objects.get_or_create(
            category=cat,
            subcategory=subcat,
            difficulty=diff,
            question_text=q_text,
            defaults={'options': opts, 'answer': ans}
        )
        if created:
            created_count += 1
    print(f'Successfully added {created_count} unique questions to AIQuestion database!')
    print(f'Total AIQuestion records in DB: {AIQuestion.objects.count()}')

if __name__ == '__main__':
    seed_db()
