# 💜 Women Thoughts System

A safe, anonymous full-stack web application designed for women to share their thoughts, seek support, and connect in a judgment-free environment.

## 🌟 Features
- **Anonymous Posting**: Share your thoughts without revealing your identity.
- **AI Empathetic Support**: Get instant, warm, and supportive replies powered by Claude AI.
- **Gender Verification**: Secure camera-based verification to ensure a safe space for women.
- **SOS Button**: Quick access to emergency helplines and a calming breathing exercise.
- **Community Feed**: Filter by category (Mental Health, Career, Relationships, etc.) and emotions.
- **Interactive Comments**: Support others through anonymous or public replies.
- **Admin Panel**: Robust moderation tools to handle reports and manage the community.

## 🛠️ Tech Stack
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism), Vanilla JavaScript.
- **Backend**: Python (Flask).
- **Database**: SQLite with SQLAlchemy ORM.
- **AI**: Anthropic Claude API (claude-3-sonnet).
- **Computer Vision**: DeepFace (for gender detection).
- **Auth**: Flask-Login + Bcrypt password hashing.

## 🚀 Installation & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/women-thoughts-system.git
cd women-thoughts-system
```

### 2. Set up a Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
1. Rename `.env.example` to `.env`.
2. Open `.env` and add your `ANTHROPIC_API_KEY` and a custom `SECRET_KEY`.

### 5. Run the Application
```bash
python app.py
```
Access the app at `http://127.0.0.1:5000`.

## 📸 Screenshots
*(Coming Soon)*
![Dashboard Screenshot Placeholder](https://via.placeholder.com/800x400?text=Women+Thoughts+Dashboard)

## 🔒 Security
- All passwords are encrypted using Bcrypt.
- CSRF protection is enabled on all forms.
- Optional gender verification ensures community integrity.

## 📄 License
This project is licensed under the MIT License.
