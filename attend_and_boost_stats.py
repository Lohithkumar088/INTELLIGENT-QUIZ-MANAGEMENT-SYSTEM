import os
import random
from datetime import timedelta
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Intelligent_Quiz.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from quizzes.models import Category, Subcategory, AIQuestion, UserQuizAttempt, UserAnswer, UserActivity

def seed_quiz_attempts_and_activity():
    users = User.objects.all()
    if not users.exists():
        print("No users found to generate attempts.")
        return

    now = timezone.now()

    categories_subcats = [
        ('Academic', 'Mathematics', 'Easy'),
        ('Academic', 'History', 'Medium'),
        ('Academic', 'Geography', 'Easy'),
        ('Academic', 'Physics', 'Medium'),
        ('Academic', 'Chemistry', 'Hard'),
        ('Academic', 'Biology', 'Easy'),
        ('Science & Tech', 'Computer Science', 'Easy'),
        ('Science & Tech', 'Artificial Intelligence', 'Medium'),
        ('Science & Tech', 'Robotics', 'Hard'),
        ('General Knowledge', 'World Facts', 'Easy'),
        ('General Knowledge', 'World Capitals', 'Easy'),
        ('Technology', 'Python Programming', 'Medium'),
        ('Technology', 'Web Development', 'Easy'),
        ('Technology', 'Cybersecurity', 'Hard'),
        ('Entertainment', 'Movies', 'Easy'),
        ('Sports & Games', 'Football', 'Easy'),
        ('Food & Health', 'Nutrition', 'Easy'),
        ('Space & Astronomy', 'Solar System', 'Medium'),
    ]

    for user in users:
        print(f"\n🚀 Generating quiz attempts and activity heatmap for: {user.username}")
        
        # 1. Generate Activity Heatmap across the last 28 days
        activity_count = 0
        for day_offset in range(27, -1, -1):
            day_date = now - timedelta(days=day_offset)

            # Generate 2 to 8 activities per day for vibrant graph colors
            num_activities_today = random.randint(2, 7)
            for k in range(num_activities_today):
                act_time = day_date.replace(hour=random.randint(8, 22), minute=random.randint(0, 59))
                cat_n, subcat_n, diff = random.choice(categories_subcats)
                
                act_type = random.choice(["Quiz Completed", "Practice Session", "Feedback Given", "Review Completed"])
                desc = f"Completed {diff} quiz in {cat_n} ({subcat_n}) with high score"
                
                act = UserActivity.objects.create(
                    user=user,
                    activity_type=act_type,
                    description=desc,
                )
                # Override timestamp date
                UserActivity.objects.filter(id=act.id).update(timestamp=act_time)
                activity_count += 1

        # 2. Generate 15 Completed Quiz Attempts with high scores (80% - 100%)
        attempt_count = 0
        for i, (cat_n, subcat_n, diff) in enumerate(categories_subcats[:15]):
            start_time = now - timedelta(days=random.randint(0, 14), hours=random.randint(1, 12))
            time_taken_seconds = random.randint(45, 180)
            end_time = start_time + timedelta(seconds=time_taken_seconds)

            # Fetch 5 or 10 questions for this topic
            qs = list(AIQuestion.objects.filter(category=cat_n, subcategory=subcat_n, difficulty=diff)[:5])
            if not qs:
                qs = list(AIQuestion.objects.filter(category=cat_n, subcategory=subcat_n)[:5])
            if not qs:
                continue

            num_qs = len(qs)
            # High score: 4 or 5 correct out of 5
            num_correct = random.choice([num_qs, num_qs - 1]) if num_qs > 1 else num_qs
            score_pct = round((num_correct / num_qs) * 100, 1)

            attempt = UserQuizAttempt.objects.create(
                user=user,
                category=cat_n,
                subcategory=subcat_n,
                difficulty=diff,
                completed=True,
                score_percentage=score_pct,
                started_at=start_time,
                completed_at=end_time
            )

            # Create UserAnswer records
            for idx, q in enumerate(qs):
                is_right = (idx < num_correct)
                user_ans = q.answer if is_right else (q.options[0] if q.options[0] != q.answer else q.options[1])
                explanation = f"Correct answer is '{q.answer}' because it directly satisfies the fundamental principle." if not is_right else ""

                UserAnswer.objects.create(
                    attempt=attempt,
                    question=q,
                    user_answer=user_ans,
                    is_correct=is_right,
                    explanation=explanation,
                    reference_link=f"https://www.google.com/search?q={q.question_text.replace(' ', '+')}",
                    learning_source="SmartLearn Knowledge Base"
                )
            
            attempt_count += 1

        print(f"✅ Generated {attempt_count} quiz attempts and {activity_count} activity records for {user.username}!")

if __name__ == '__main__':
    seed_quiz_attempts_and_activity()
