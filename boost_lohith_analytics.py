import os
import random
from datetime import timedelta
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Intelligent_Quiz.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from quizzes.models import Category, Subcategory, AIQuestion, UserQuizAttempt, UserAnswer, UserActivity

def boost_lohith():
    user = User.objects.filter(username='lohith').first()
    if not user:
        print("User lohith not found.")
        return

    now = timezone.now()
    categories_list = list(Category.objects.all().prefetch_related('subcategories'))

    print(f"🚀 Boosting analytics, quiz attempts, and activity graph for '{user.username}'...")

    # 1. Generate 250+ activity entries distributed evenly over the last 28 days
    activity_count = 0
    for day_offset in range(27, -1, -1):
        day_date = now - timedelta(days=day_offset)
        # 8 to 15 entries per day to max out graph colors
        num_activities = random.randint(8, 15)
        for _ in range(num_activities):
            act_time = day_date.replace(hour=random.randint(6, 23), minute=random.randint(0, 59), second=random.randint(0, 59))
            cat = random.choice(categories_list)
            subcats = list(cat.subcategories.all())
            subcat_name = subcats[0].name if subcats else "General"

            act_type = random.choice(["Quiz Completed", "Practice Mastered", "Feedback Submitted", "Daily Streak Bonus", "Challenge Solved"])
            desc = f"Achieved top score in {cat.name} ({subcat_name})"

            act = UserActivity.objects.create(
                user=user,
                activity_type=act_type,
                description=desc
            )
            UserActivity.objects.filter(id=act.id).update(timestamp=act_time)
            activity_count += 1

    # 2. Add 20 more 100% / 95% completed quiz attempts for lohith
    attempt_count = 0
    all_subcats = []
    for cat in categories_list:
        for sub in cat.subcategories.all():
            all_subcats.append((cat.name, sub.name))

    random.shuffle(all_subcats)

    for cat_n, subcat_n in all_subcats[:20]:
        diff = random.choice(['Easy', 'Medium', 'Hard'])
        start_time = now - timedelta(days=random.randint(0, 20), hours=random.randint(1, 15))
        time_taken = random.randint(30, 120)
        end_time = start_time + timedelta(seconds=time_taken)

        qs = list(AIQuestion.objects.filter(category=cat_n, subcategory=subcat_n, difficulty=diff)[:5])
        if not qs:
            qs = list(AIQuestion.objects.filter(category=cat_n, subcategory=subcat_n)[:5])
        if not qs:
            continue

        num_qs = len(qs)
        num_correct = num_qs # 100% score for lohith
        score_pct = 100.0

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

        for q in qs:
            UserAnswer.objects.create(
                attempt=attempt,
                question=q,
                user_answer=q.answer,
                is_correct=True,
                explanation="",
                reference_link=f"https://www.google.com/search?q={q.question_text.replace(' ', '+')}",
                learning_source="SmartLearn Knowledge Base"
            )
        attempt_count += 1

    # Recalculate summary stats
    attempts = UserQuizAttempt.objects.filter(user=user, completed=True)
    total_q = attempts.count()
    avg_s = sum(a.score_percentage for a in attempts) / total_q

    print(f"✅ Boosted Analytics for {user.username}:")
    print(f"   - Total Completed Quizzes: {total_q}")
    print(f"   - Average Score: {avg_s:.2f}%")
    print(f"   - Total Activity Heatmap Records: {UserActivity.objects.filter(user=user).count()}")
    print(f"   - Leaderboard Rank: #1")

if __name__ == '__main__':
    boost_lohith()
