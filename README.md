Voxia AI Assistant

Voxia is a smart AI-powered web assistant built using Flask that combines automation, system control, and AI responses in one platform.

---

Features

* User Authentication (Signup/Login)
* Chat-based AI Assistant
* Open Websites (Google, YouTube)
* Search Google & YouTube
* Weather Updates
* Latest News Headlines
* Multi-language Translation
* Code Generation (AI-powered)
* System Controls (Volume, Brightness)
* Screenshot Capture
* Chat History Storage (SQLite)

---

Tech Stack

* Backend: Python, Flask
* Frontend: HTML, CSS, JavaScript
* Database: SQLite
* AI Integration: Hugging Face API
* Libraries:

  * requests
  * pyautogui
  * feedparser
  * deep_translator
  * screen_brightness_control

---

Project Structure

```
Voxia-AI-Assistant/
│
├── app.py
├── users.db
├── requirements.txt
├── .env (not included in repo)
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   └── dashboard.html
│
├── static/
│   ├── style.css
│   ├── script.js
│   ├── dashboard.css
│   └── dashboard.js
```

---

Setup Instructions

1. Clone Repository

```bash
git clone https://github.com/akumallavidhya/Voxia-AI-Assisstant.git
cd Voxia-AI-Assisstant
```

---

2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

3. Setup Environment Variables

Create a `.env` file:

```
HF_TOKEN=your_huggingface_token_here
```

---

4. Run the App

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000/
```

---

How AI Works

* Uses Hugging Face Inference API
* Handles:

  * General questions
  * Code generation
  * Smart responses

---

Security Note

* `.env` file is excluded from GitHub using `.gitignore`
* Never expose API tokens publicly

---

 Future Improvements

* Voice assistant integration
* Better AI response accuracy
* Deployment (Render / Railway)
* Mobile responsiveness
* Dark/light theme toggle

---

Author

Vidhya Sree Akumalla

---

