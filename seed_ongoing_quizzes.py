import os
from datetime import timedelta
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Intelligent_Quiz.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from quizzes.models import UserQuizAttempt, AIQuestion, UserAnswer

def seed_ongoing_quizzes():
    users = User.objects.filter(username__in=['lohith', 'student'])

    ongoing_specs = [
        ('Technology', 'Cybersecurity', 'Hard'),
        ('Science & Tech', 'Robotics', 'Medium'),
        ('Academic', 'Physics', 'Medium'),
        ('Culture & Heritage', 'Ancient Civilizations', 'Easy'),
    ]

    now = timezone.now()

    for user in users:
        print(f"⌛ Creating ongoing quizzes for user: {user.username}")
        for i, (cat, sub, diff) in enumerate(ongoing_specs):
            start_time = now - timedelta(minutes=10 * (i + 1))

            attempt = UserQuizAttempt.objects.create(
                user=user,
                category=cat,
                subcategory=sub,
                difficulty=diff,
                completed=False,
                score_percentage=0,
                started_at=start_time
            )

            # Add 2 answered questions out of 5 to simulate partial progress
            qs = list(AIQuestion.objects.filter(category=cat, subcategory=sub, difficulty=diff)[:2])
            for q in qs:
                UserAnswer.objects.create(
                    attempt=attempt,
                    question=q,
                    user_answer=q.options[0],
                    is_correct=(q.options[0] == q.answer),
                    explanation="",
                    reference_link="",
                    learning_source=""
                )

            print(f"   - Added ongoing attempt #{attempt.id}: {cat} > {sub} ({diff})")

if __name__ == '__main__':
    seed_ongoing_quizzes()
