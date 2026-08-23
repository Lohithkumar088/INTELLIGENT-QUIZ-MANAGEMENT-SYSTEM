# AWS Hosting Guide - Intelligent Quiz Management System

This guide explains how to host your Django project on **AWS (Amazon Web Services)**.

---

## Method 1: AWS EC2 + Nginx + Gunicorn (Recommended - Free Tier Eligible & Full Control)

### Step 1: Launch an EC2 Instance on AWS
1. Log in to [AWS Management Console](https://aws.amazon.com/console/).
2. Go to **EC2** → Click **Launch Instance**.
3. Name: `Intelligent-Quiz-Server`
4. Application OS: **Ubuntu 24.04 LTS** (or 22.04 LTS).
5. Instance Type: **t2.micro** or **t3.micro** *(Free tier eligible)*.
6. Key Pair: Click **Create new key pair** (e.g. `quiz-key.pem`) and download it to your Mac.
7. Network / Security Group Rules: Check all three boxes:
   - ✅ Allow SSH traffic from anywhere (Port 22)
   - ✅ Allow HTTP traffic from the internet (Port 80)
   - ✅ Allow HTTPS traffic from the internet (Port 443)
8. Click **Launch Instance**.

---

### Step 2: Connect to Your EC2 Instance
Open Terminal on your Mac and run:

```bash
# Navigate to where your key pair was downloaded (e.g., Downloads):
cd ~/Downloads
chmod 400 quiz-key.pem

# SSH into your EC2 instance (Replace <EC2-PUBLIC-IP> with your EC2 Public IP address):
ssh -i "quiz-key.pem" ubuntu@<EC2-PUBLIC-IP>
```

---

### Step 3: Install Packages & Clone GitHub Repository
Once connected inside your EC2 server:

```bash
# Update server packages:
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx git -y

# Clone your GitHub repository:
git clone https://github.com/lohithkumar088/INTELLIGENT-QUIZ-MANAGEMENT-SYSTEM.git
cd INTELLIGENT-QUIZ-MANAGEMENT-SYSTEM

# Create virtual environment and install dependencies:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run build setup (collects static files, runs migrations & seeds 4,100 questions):
chmod +x build.sh
./build.sh
```

---

### Step 4: Configure Gunicorn Service

Create a systemd service file for Gunicorn:

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Paste the following configuration:

```ini
[Unit]
Description=gunicorn daemon for Intelligent Quiz System
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/INTELLIGENT-QUIZ-MANAGEMENT-SYSTEM
ExecStart=/home/ubuntu/INTELLIGENT-QUIZ-MANAGEMENT-SYSTEM/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/INTELLIGENT-QUIZ-MANAGEMENT-SYSTEM/app.sock Intelligent_Quiz.wsgi:application

[Install]
WantedBy=multi-user.target
```

Save and exit (`Ctrl + O`, `Enter`, `Ctrl + X`).

Start and enable Gunicorn:
```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

---

### Step 5: Configure Nginx Web Server

Create Nginx site configuration:

```bash
sudo nano /etc/nginx/sites-available/quiz
```

Paste the following configuration (Replace `<EC2-PUBLIC-IP>` with your instance's Public IP):

```nginx
server {
    listen 80;
    server_name <EC2-PUBLIC-IP>;

    location /static/ {
        alias /home/ubuntu/INTELLIGENT-QUIZ-MANAGEMENT-SYSTEM/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/INTELLIGENT-QUIZ-MANAGEMENT-SYSTEM/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/INTELLIGENT-QUIZ-MANAGEMENT-SYSTEM/app.sock;
    }
}
```

Save and exit (`Ctrl + O`, `Enter`, `Ctrl + X`).

Enable site & restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/quiz /etc/nginx/sites-enabled/
sudo unlink /etc/nginx/sites-enabled/default 2>/dev/null
sudo nginx -t
sudo systemctl restart nginx
```

🎉 Your Django application is now live on AWS EC2 at `http://<EC2-PUBLIC-IP>`!

---

## Method 2: AWS App Runner (PaaS - Easiest & Auto-deploy from GitHub)

If you prefer zero server management:

1. Log in to **AWS Console** → Search for **AWS App Runner**.
2. Click **Create Service**.
3. Source: **Source code repository** → Connect your GitHub account and select `INTELLIGENT-QUIZ-MANAGEMENT-SYSTEM`.
4. Build settings:
   - **Runtime:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn Intelligent_Quiz.wsgi:application`
   - **Port:** `8000`
5. Click **Create & Deploy**.

AWS App Runner will automatically deploy your GitHub code and provide an SSL `https://...` link!
