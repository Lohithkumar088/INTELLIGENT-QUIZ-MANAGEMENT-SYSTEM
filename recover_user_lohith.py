import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Intelligent_Quiz.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile
from quizzes.models import UserQuizAttempt, UserActivity

def recover_lohith():
    username = 'lohith'
    password = 'yathvika'
    email = 'lohith@example.com'

    # Create or update user lohith
    user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'is_staff': True, 'is_superuser': True})
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()

    Profile.objects.get_or_create(user=user)

    print(f"✅ Recovered User account '{username}' with password '{password}'!")

    # Transfer top attempts and activity from admin/student to lohith so lohith becomes Rank #1!
    admin_user = User.objects.filter(username='admin').first()
    if admin_user:
        attempts_reassigned = UserQuizAttempt.objects.filter(user=admin_user).update(user=user)
        activities_reassigned = UserActivity.objects.filter(user=admin_user).update(user=user)
        print(f"✅ Reassigned {attempts_reassigned} quiz attempts and {activities_reassigned} activity records to '{username}'!")

    # Verify rank
    from django.db.models import Avg
    ranked_users = (
        UserQuizAttempt.objects.filter(completed=True)
        .values('user')
        .annotate(avg_score=Avg('score_percentage'))
        .order_by('-avg_score')
    )
    for idx, entry in enumerate(ranked_users, start=1):
        u = User.objects.get(id=entry['user'])
        print(f"Rank #{idx}: Username={u.username}, AvgScore={entry['avg_score']:.2f}%")

if __name__ == '__main__':
    recover_lohith()
