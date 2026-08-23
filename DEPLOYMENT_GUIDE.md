# Deployment & GitHub Hosting Guide

Follow these steps to host your **Intelligent Quiz Management System** on GitHub and make it live online on the web.

---

## 1. Push Project Code to GitHub

### Step 1: Create a New Repository on GitHub
1. Go to [GitHub - New Repository](https://github.com/new).
2. Set Repository Name: `INTELLIGENT-QUIZ-MANAGEMENT-SYSTEM`
3. Select **Public** (or **Private**).
4. Click **Create repository** *(Do NOT check "Add a README file" as one is already included)*.

### Step 2: Push Code from Mac Terminal
Open Terminal on your Mac and run the following commands:

```bash
cd "/Users/lohith/MY PROJECTS/INTELLIGENT-QUIZ-MANAGEMENT-SYSTEM-USING-AI-main"

# Link your local repository to your GitHub repository URL:
git remote add origin https://github.com/lohithkumar088/INTELLIGENT-QUIZ-MANAGEMENT-SYSTEM.git

# Push code to main branch:
git branch -M main
git push -u origin main
```

---

## 2. Deploy Live Online (Free Deployment on Render)

To make your Django app live with a public domain URL accessible worldwide:

1. Sign up or log in at [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** → **Web Service**.
3. Select **Build and deploy from a Git repository** and connect your GitHub account.
4. Select your **`INTELLIGENT-QUIZ-MANAGEMENT-SYSTEM`** repository.
5. Fill in the deployment settings:
   - **Name:** `intelligent-quiz-management-system`
   - **Region:** Any (e.g., Oregon, Singapore, Frankfurt)
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn Intelligent_Quiz.wsgi:application`
6. Click **Create Web Service**.

Render will automatically install requirements, run database migrations, seed the 4,100 quiz questions, and publish your site live with a free SSL certificate!
